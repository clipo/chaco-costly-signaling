#!/usr/bin/env python3
"""Download academic papers through institutional EZproxy or open access.

A portable, config-driven script for acquiring PDFs of academic references.
Supports 8 publisher-specific extractors, open access pre-check, EZproxy
authentication, and print-to-PDF fallback.

Subcommands:
    init        Create a new config file with default settings
    add         Add a paper entry to the config
    status      Show download status for all papers in the config
    download    Download pending papers (default)

Usage:
    python3 download_papers.py init --config papers_config.json
    python3 download_papers.py add --doi 10.1234/example --filename Author_2024.pdf
    python3 download_papers.py status
    python3 download_papers.py download
    python3 download_papers.py download --headed --only "Smith"
    python3 download_papers.py download --dry-run

EZproxy session cookies don't persist to disk, so the script always opens
a visible Chrome window first for login, then downloads in that session.
"""

import argparse
import base64
import glob
import json
import os
import platform
import re
import shutil
import signal
import subprocess
import sys
import tempfile
import time
from pathlib import Path

DEFAULT_CONFIG = "papers_config.json"

CONFIG_TEMPLATE = {
    "ezproxy_base": "https://login.proxy.binghamton.edu/login?url=",
    "output_dir": ".",
    "min_valid_size_bytes": 10000,
    "papers": []
}

PAPER_TEMPLATE = {
    "filename": "",
    "doi": None,
    "url": None,
    "oa_url": None,
    "status": "pending",
    "note": ""
}


# ── Config I/O ──────────────────────────────────────────────────────────

def load_config(config_path):
    """Load and validate the JSON config file."""
    path = Path(config_path)
    if not path.exists():
        print(f"ERROR: Config file not found: {config_path}")
        print(f"  Run: python3 {sys.argv[0]} init --config {config_path}")
        sys.exit(1)
    with open(path) as f:
        config = json.load(f)
    # Validate required fields
    for key in ("ezproxy_base", "output_dir", "papers"):
        if key not in config:
            print(f"ERROR: Config missing required key '{key}'")
            sys.exit(1)
    if "min_valid_size_bytes" not in config:
        config["min_valid_size_bytes"] = 10000
    return config


def save_config(config, config_path):
    """Write config back to disk, preserving human-readable formatting."""
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)
        f.write("\n")


# ── Chrome auto-detection ───────────────────────────────────────────────

def find_chrome():
    """Find the Chrome/Chromium binary. Returns path or exits with error."""
    # Check PATH first
    for name in ("google-chrome", "google-chrome-stable", "chromium",
                 "chromium-browser", "chrome"):
        found = shutil.which(name)
        if found:
            return found

    # Common install locations
    candidates = [
        "/opt/google/chrome/chrome",
        "/opt/google/chrome/google-chrome",
        "/usr/bin/google-chrome",
        "/usr/bin/google-chrome-stable",
        "/usr/bin/chromium",
        "/usr/bin/chromium-browser",
        "/snap/bin/chromium",
    ]
    if platform.system() == "Darwin":
        candidates.extend([
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            "/Applications/Chromium.app/Contents/MacOS/Chromium",
        ])

    for path in candidates:
        if os.path.isfile(path) and os.access(path, os.X_OK):
            return path

    print("ERROR: Chrome/Chromium not found.")
    print("  Install Chrome or set the path in the script.")
    sys.exit(1)


# ── Chrome / Selenium plumbing ──────────────────────────────────────────

def launch_chrome(chrome_path, headed=False):
    """Launch Chrome with a temp profile and remote debugging port.

    Returns (subprocess.Popen, debug_port).
    """
    tmp_profile = tempfile.mkdtemp(prefix="chrome_ezproxy_")

    cmd = [
        chrome_path,
        f"--user-data-dir={tmp_profile}",
        "--remote-debugging-port=0",
        "--no-first-run",
        "--disable-extensions",
        "--disable-gpu",
        "--no-sandbox",
        "--disable-dev-shm-usage",
        "about:blank",
    ]
    if not headed:
        cmd.insert(1, "--headless=new")

    stderr_file = Path(tempfile.gettempdir()) / "chrome_dl_stderr.txt"
    stderr_fh = open(stderr_file, "w")
    proc = subprocess.Popen(
        cmd, stdout=subprocess.DEVNULL, stderr=stderr_fh)

    debug_port = None
    deadline = time.time() + 45
    while time.time() < deadline:
        time.sleep(0.5)
        if proc.poll() is not None:
            stderr_fh.close()
            raise RuntimeError(
                f"Chrome exited unexpectedly. Stderr:\n"
                f"{stderr_file.read_text()[-500:]}")
        try:
            content = stderr_file.read_text()
        except Exception:
            continue
        match = re.search(
            r'DevTools listening on ws://127\.0\.0\.1:(\d+)/', content)
        if match:
            debug_port = int(match.group(1))
            break

    stderr_fh.close()
    if debug_port is None:
        proc.kill()
        raise RuntimeError(
            f"Could not find Chrome debug port. Stderr:\n"
            f"{stderr_file.read_text()[-500:]}")

    return proc, debug_port


def connect_selenium(debug_port):
    """Connect Selenium to a running Chrome instance via its debug port."""
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options

    options = Options()
    options.add_experimental_option(
        "debuggerAddress", f"127.0.0.1:{debug_port}")
    return webdriver.Chrome(options=options)


def configure_downloads(driver, download_dir):
    """Configure Chrome to auto-download PDFs instead of rendering them."""
    driver.execute_cdp_cmd("Page.setDownloadBehavior", {
        "behavior": "allow",
        "downloadPath": download_dir,
    })


# ── Download helpers ────────────────────────────────────────────────────

def wait_for_download(download_dir, timeout=45):
    """Wait for any .crdownload file to finish."""
    start = time.time()
    time.sleep(2)
    while time.time() - start < timeout:
        crdownloads = glob.glob(os.path.join(download_dir, "*.crdownload"))
        if crdownloads:
            time.sleep(1)
            continue
        return True
    return False


def find_new_file(download_dir, before_files):
    """Find a file that appeared since before_files snapshot."""
    current = set(os.listdir(download_dir))
    new_files = current - before_files
    pdfs = [f for f in new_files if f.lower().endswith('.pdf')]
    if pdfs:
        return pdfs[0]
    others = [f for f in new_files if not f.endswith('.crdownload')]
    return others[0] if others else None


def try_oa_download(oa_url, output_path, min_size):
    """Try to download a PDF from an open access URL.

    Returns True if a valid PDF was saved.
    """
    import requests

    try:
        resp = requests.get(oa_url, timeout=30, allow_redirects=True,
                            headers={"User-Agent": "academic-downloader/1.0"})
        if resp.status_code == 200 and len(resp.content) > min_size:
            # Check PDF magic bytes
            if resp.content[:4] == b'%PDF':
                output_path.write_bytes(resp.content)
                return True
    except Exception:
        pass
    return False


# ── Publisher-specific PDF extractors ───────────────────────────────────

def try_get_pdf(driver):
    """Try to find and navigate to a PDF download link on the current page.

    Supports: ScienceDirect, Wiley, Nature, Springer, JSTOR,
    Taylor & Francis, Cell Press, UChicago Press, plus HTML link fallback.

    Returns True if navigation was attempted.
    """
    url = driver.current_url.lower()

    # ScienceDirect (Elsevier)
    if 'sciencedirect' in url:
        pii = re.search(
            r'/pii/([A-Z0-9]+)', driver.current_url, re.IGNORECASE)
        if pii:
            base = driver.current_url.split('/science/')[0]
            driver.get(
                f"{base}/science/article/pii/{pii.group(1)}/pdfft"
                f"?isDTMRedir=true&download=true")
            return True

    # Wiley
    if 'wiley' in url or 'onlinelibrary' in url:
        doi = re.search(
            r'/doi/(?:full|abs|epdf|)/?([^?]+)', driver.current_url)
        if doi:
            base = driver.current_url.split('/doi/')[0]
            driver.get(
                f"{base}/doi/pdfdirect/{doi.group(1)}?download=true")
            return True

    # Nature
    if 'nature' in url and '/articles/' in url:
        clean = driver.current_url.split('?')[0].rstrip('/')
        if not clean.endswith('.pdf'):
            driver.get(clean + '.pdf')
            return True

    # Springer
    if 'springer' in url or 'link.springer' in url:
        doi = re.search(r'/(10\.\d+/[^?#]+)', driver.current_url)
        if doi:
            base = re.match(
                r'(https?://[^/]+)', driver.current_url).group(1)
            driver.get(f"{base}/content/pdf/{doi.group(1)}.pdf")
            return True

    # JSTOR
    if 'jstor' in url:
        stable = re.search(
            r'/stable/(?:pdf/)?(\d+)', driver.current_url)
        if stable:
            base = re.match(
                r'(https?://[^/]+)', driver.current_url).group(1)
            driver.get(f"{base}/stable/pdf/{stable.group(1)}.pdf")
            return True

    # Taylor & Francis
    if 'tandfonline' in url:
        doi = re.search(
            r'/doi/(?:full|abs|)/?([^?]+)', driver.current_url)
        if doi:
            base = driver.current_url.split('/doi/')[0]
            driver.get(
                f"{base}/doi/pdf/{doi.group(1)}?download=true")
            return True

    # Cell Press (e.g., TREE, Current Biology)
    if 'cell.com' in url:
        pii = re.search(
            r'/(S\d{4}-\d+\(\d+\)\d+-\w)', driver.current_url)
        if pii:
            base = re.match(
                r'(https?://[^/]+)', driver.current_url).group(1)
            driver.get(
                f"{base}/action/showPdf?pii={pii.group(1)}")
            return True

    # UChicago Press
    if 'uchicago' in url:
        doi = re.search(
            r'/doi/(?:full|abs|)/?([^?]+)', driver.current_url)
        if doi:
            base = driver.current_url.split('/doi/')[0]
            driver.get(f"{base}/doi/pdf/{doi.group(1)}")
            return True

    # Fallback: look for PDF links in the page HTML
    try:
        from selenium.webdriver.common.by import By
        links = driver.find_elements(By.TAG_NAME, "a")
        for link in links:
            try:
                href = link.get_attribute("href") or ""
                text = link.text.lower().strip()
            except Exception:
                continue
            if text in ("pdf", "download pdf", "get pdf",
                        "full text pdf", "view pdf", "save pdf"):
                driver.get(href)
                return True
    except Exception:
        pass

    return False


# ── Core download logic ─────────────────────────────────────────────────

def download_paper(driver, paper, output_dir, min_size, ezproxy_base):
    """Navigate to a paper and download its PDF.

    Args:
        driver: Selenium WebDriver connected to Chrome.
        paper: Dict with keys filename, doi, url, oa_url.
        output_dir: Path to the download directory.
        min_size: Minimum valid file size in bytes.
        ezproxy_base: EZproxy login prefix URL.

    Returns:
        (success: bool, note: str)
    """
    filename = paper["filename"]
    filepath = Path(output_dir) / filename

    if filepath.exists() and filepath.stat().st_size > min_size:
        return True, f"on disk, {filepath.stat().st_size:,} bytes"

    download_dir = str(output_dir)
    before_files = set(os.listdir(download_dir))

    # Build the URL to navigate to
    if paper.get("url"):
        nav_url = ezproxy_base + paper["url"]
    elif paper.get("doi"):
        nav_url = ezproxy_base + f"https://doi.org/{paper['doi']}"
    else:
        return False, "no DOI or URL"

    # Navigate
    print(f"  Loading EZproxy URL...")
    try:
        driver.get(nav_url)
    except Exception as e:
        return False, f"navigation error: {e}"

    time.sleep(6)
    current_url = driver.current_url
    print(f"  Landed: {current_url[:100]}")

    # Check for auth redirect (Binghamton-specific patterns, but other
    # institutions typically redirect to a login page too)
    if any(x in current_url for x in
           ('cas.cc.binghamton', 'shibboleth', '/login?')):
        # Only flag as session-expired if we're on an auth page,
        # not just any URL with /login in it
        if 'cas.cc.binghamton' in current_url or 'shibboleth' in current_url:
            return False, "session expired"

    # Check if a PDF was auto-downloaded
    wait_for_download(download_dir, timeout=5)
    new_file = find_new_file(download_dir, before_files)
    if new_file:
        src = Path(output_dir) / new_file
        dst = Path(output_dir) / filename
        if src != dst:
            if dst.exists():
                dst.unlink()
            src.rename(dst)
        return True, f"auto-download ({dst.stat().st_size:,} bytes)"

    # Try publisher-specific PDF URL
    before_files = set(os.listdir(download_dir))
    if try_get_pdf(driver):
        time.sleep(4)
        wait_for_download(download_dir, timeout=30)
        new_file = find_new_file(download_dir, before_files)
        if new_file:
            src = Path(output_dir) / new_file
            dst = Path(output_dir) / filename
            if src != dst:
                if dst.exists():
                    dst.unlink()
                src.rename(dst)
            return True, f"publisher ({dst.stat().st_size:,} bytes)"

        # PDF might have rendered in-browser; capture via print-to-PDF
        try:
            pdf_data = driver.execute_cdp_cmd("Page.printToPDF", {
                "printBackground": True,
                "preferCSSPageSize": True,
            })
            content = base64.b64decode(pdf_data['data'])
            if len(content) > min_size:
                filepath.write_bytes(content)
                return True, f"print-to-PDF ({len(content):,} bytes)"
        except Exception:
            pass

    return False, "could not download"


# ── Subcommand handlers ─────────────────────────────────────────────────

def cmd_init(args):
    """Create a new config file with default settings."""
    config_path = Path(args.config)
    if config_path.exists() and not args.force:
        print(f"ERROR: {args.config} already exists. Use --force to overwrite.")
        sys.exit(1)
    save_config(CONFIG_TEMPLATE.copy(), args.config)
    print(f"Created {args.config}")
    print(f"  Edit it directly or use: python3 {sys.argv[0]} add --doi ...")


def cmd_add(args):
    """Add a paper entry to the config."""
    config = load_config(args.config)
    entry = PAPER_TEMPLATE.copy()
    entry["filename"] = args.filename
    if args.doi:
        entry["doi"] = args.doi
    if args.url:
        entry["url"] = args.url
    if args.oa_url:
        entry["oa_url"] = args.oa_url

    # Check for duplicate filename
    existing = [p["filename"] for p in config["papers"]]
    if entry["filename"] in existing:
        print(f"WARNING: {entry['filename']} already in config, adding anyway")

    config["papers"].append(entry)
    save_config(config, args.config)
    print(f"Added {entry['filename']} ({len(config['papers'])} total)")


def cmd_status(args):
    """Show download status for all papers in the config."""
    config = load_config(args.config)
    output_dir = Path(config["output_dir"])
    min_size = config.get("min_valid_size_bytes", 10000)

    if not config["papers"]:
        print("No papers in config.")
        return

    counts = {"pending": 0, "downloaded": 0, "failed": 0, "skipped": 0}
    for paper in config["papers"]:
        filename = paper["filename"]
        filepath = output_dir / filename
        status = paper.get("status", "pending")

        # Check actual disk state
        if filepath.exists() and filepath.stat().st_size > min_size:
            disk = f"ON DISK  {filepath.stat().st_size:>10,} B"
            effective = "downloaded"
        elif filepath.exists():
            disk = f"TOO SMALL {filepath.stat().st_size:>9,} B"
            effective = status
        else:
            disk = "MISSING               "
            effective = status if status != "downloaded" else "missing"

        counts[effective] = counts.get(effective, 0) + 1
        status_tag = f"[{disk}] [{status:>10}]"
        print(f"  {status_tag} {filename}")
        if paper.get("note"):
            print(f"    note: {paper['note']}")

    print()
    total = len(config["papers"])
    on_disk = sum(1 for p in config["papers"]
                  if (output_dir / p["filename"]).exists()
                  and (output_dir / p["filename"]).stat().st_size > min_size)
    pending = total - on_disk
    print(f"  {on_disk}/{total} on disk, {pending} remaining")


def cmd_download(args):
    """Download pending papers."""
    config = load_config(args.config)
    output_dir = Path(config["output_dir"])
    min_size = config.get("min_valid_size_bytes", 10000)
    ezproxy_base = config.get("ezproxy_base", "")

    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)

    # Filter papers
    papers = config["papers"]
    if args.only:
        papers = [p for p in papers
                  if args.only.lower() in p["filename"].lower()]
        if not papers:
            print(f"No papers match filter '{args.only}'")
            sys.exit(1)

    # Filter to pending/failed only (skip already downloaded)
    pending = []
    for p in papers:
        filepath = output_dir / p["filename"]
        if filepath.exists() and filepath.stat().st_size > min_size:
            continue
        pending.append(p)

    if not pending and not args.dry_run:
        print("All papers already downloaded.")
        return

    if args.dry_run:
        for p in papers:
            filepath = output_dir / p["filename"]
            if filepath.exists() and filepath.stat().st_size > min_size:
                print(f"  [ON DISK  {filepath.stat().st_size:>10,} B] "
                      f"{p['filename']}")
            elif filepath.exists():
                print(f"  [TOO SMALL {filepath.stat().st_size:>9,} B] "
                      f"{p['filename']}")
            else:
                print(f"  [MISSING                ] {p['filename']}")
        on_disk = sum(1 for p in papers
                      if (output_dir / p["filename"]).exists()
                      and (output_dir / p["filename"]).stat().st_size
                      > min_size)
        print(f"\n{len(papers) - on_disk} of {len(papers)} still needed")
        return

    # ── Phase 1: Open access pre-check ──────────────────────────────
    oa_papers = [p for p in pending if p.get("oa_url")]
    if oa_papers:
        print(f"\n── Open access pre-check ({len(oa_papers)} papers) ──\n")
        try:
            import requests  # noqa: F811
        except ImportError:
            print("  WARNING: 'requests' not installed, skipping OA check")
            oa_papers = []

        oa_ok = 0
        for p in oa_papers:
            filepath = output_dir / p["filename"]
            print(f"  {p['filename']}... ", end="", flush=True)
            if try_oa_download(p["oa_url"], filepath, min_size):
                p["status"] = "downloaded"
                p["note"] = "open access"
                save_config(config, args.config)
                print(f"OK ({filepath.stat().st_size:,} bytes)")
                oa_ok += 1
                pending.remove(p)
            else:
                print("not available, will try EZproxy")
        if oa_ok:
            print(f"\n  {oa_ok} downloaded via open access\n")

    # Recheck: anything left to download via EZproxy?
    still_pending = [p for p in pending
                     if not ((output_dir / p["filename"]).exists()
                             and (output_dir / p["filename"]).stat().st_size
                             > min_size)]
    if not still_pending:
        print("All papers downloaded (open access).")
        return

    # ── Phase 2: EZproxy downloads ──────────────────────────────────
    if not ezproxy_base:
        print("WARNING: No ezproxy_base configured. Skipping EZproxy phase.")
        print(f"  {len(still_pending)} papers still need downloading.")
        return

    chrome_path = find_chrome()
    print(f"\nUsing Chrome: {chrome_path}")

    chrome_proc = None
    ok, fail = 0, 0
    failed = []
    try:
        # Always launch headed for EZproxy login
        chrome_proc, debug_port = launch_chrome(chrome_path, headed=True)
        print(f"Chrome debug port: {debug_port}")

        time.sleep(3)

        print("Connecting Selenium...")
        driver = connect_selenium(debug_port)
        configure_downloads(driver, str(output_dir))

        # Check EZproxy session using the first pending paper's DOI
        first_doi = None
        for p in still_pending:
            if p.get("doi"):
                first_doi = p["doi"]
                break
        if first_doi:
            test_url = ezproxy_base + f"https://doi.org/{first_doi}"
        else:
            # Fallback: use any URL from the first paper
            test_url = ezproxy_base + (
                still_pending[0].get("url", "https://doi.org/10.1234/test"))

        print("Checking EZproxy session...")
        driver.get(test_url)
        time.sleep(5)

        if 'cas.cc.binghamton' in driver.current_url or \
                'shibboleth' in driver.current_url:
            print()
            print("Log in to EZproxy in the Chrome window.")
            print("Waiting for login to complete...")
            login_deadline = time.time() + 300
            while time.time() < login_deadline:
                try:
                    current = driver.current_url
                except Exception:
                    time.sleep(2)
                    continue
                if ('cas.cc.binghamton' not in current
                        and 'shibboleth' not in current):
                    break
                time.sleep(2)
            else:
                print("ERROR: Login timed out (5 minutes). Aborting.")
                driver.quit()
                chrome_proc.terminate()
                sys.exit(1)
            time.sleep(3)
        print("EZproxy session is active.")

        # If the test URL already loaded a paper, switch to headed/headless
        if not args.headed:
            # Re-configure after potential login navigation
            configure_downloads(driver, str(output_dir))

        # Download papers
        print(f"\nDownloading {len(still_pending)} papers to {output_dir}\n")

        for i, paper in enumerate(still_pending, 1):
            print(f"[{i}/{len(still_pending)}] {paper['filename']}")
            success, note = download_paper(
                driver, paper, output_dir, min_size, ezproxy_base)
            if success:
                paper["status"] = "downloaded"
                paper["note"] = note
                ok += 1
                print(f"  OK {note}")
            else:
                paper["status"] = "failed"
                paper["note"] = note
                fail += 1
                failed.append(paper)
                print(f"  FAIL ({note})")

            # Save status after each paper
            save_config(config, args.config)

            if i < len(still_pending):
                time.sleep(2)

        driver.quit()

    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if chrome_proc:
            chrome_proc.terminate()
            try:
                chrome_proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                chrome_proc.kill()

    # Summary
    print(f"\n{'=' * 60}")
    print(f"Results: {ok} succeeded, {fail} failed")
    if failed:
        print(f"\nFailed ({len(failed)}):")
        for p in failed:
            doi_str = p.get('doi', p.get('url', 'no DOI/URL'))
            print(f"  {p['filename']}  ({doi_str})")
            if p.get("note"):
                print(f"    reason: {p['note']}")
    print()


# ── CLI argument parsing ────────────────────────────────────────────────

def build_parser():
    """Build the argument parser with subcommands."""
    # Shared --config argument via parent parser
    config_parent = argparse.ArgumentParser(add_help=False)
    config_parent.add_argument(
        "--config", type=str, default=DEFAULT_CONFIG,
        help=f"Path to config file (default: {DEFAULT_CONFIG})")

    parser = argparse.ArgumentParser(
        description="Download academic papers via EZproxy and open access.",
        formatter_class=argparse.RawDescriptionHelpFormatter)

    subparsers = parser.add_subparsers(dest="command")

    # init
    p_init = subparsers.add_parser(
        "init", help="Create a new config file",
        parents=[config_parent])
    p_init.add_argument(
        "--force", action="store_true",
        help="Overwrite existing config file")

    # add
    p_add = subparsers.add_parser(
        "add", help="Add a paper to the config",
        parents=[config_parent])
    p_add.add_argument(
        "--filename", required=True,
        help="Output filename (e.g. Author_Year.pdf)")
    p_add.add_argument(
        "--doi", default=None,
        help="DOI (e.g. 10.1234/example)")
    p_add.add_argument(
        "--url", default=None,
        help="Direct URL (used if DOI is not available)")
    p_add.add_argument(
        "--oa-url", dest="oa_url", default=None,
        help="Open access URL to try before EZproxy")

    # status
    subparsers.add_parser(
        "status", help="Show download status",
        parents=[config_parent])

    # download
    p_dl = subparsers.add_parser(
        "download", help="Download pending papers",
        parents=[config_parent])
    p_dl.add_argument(
        "--headed", action="store_true",
        help="Keep browser visible during downloads")
    p_dl.add_argument(
        "--dry-run", action="store_true",
        help="List papers without downloading")
    p_dl.add_argument(
        "--only", type=str, default=None,
        help="Only download papers whose filename contains this substring")

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    # Default to 'download' if no subcommand given
    if args.command is None:
        # No subcommand: default to download with default config
        args.config = DEFAULT_CONFIG
        if not Path(args.config).exists():
            parser.print_help()
            sys.exit(1)
        args.command = "download"
        args.headed = False
        args.dry_run = False
        args.only = None

    if args.command == "init":
        cmd_init(args)
    elif args.command == "add":
        cmd_add(args)
    elif args.command == "status":
        cmd_status(args)
    elif args.command == "download":
        cmd_download(args)


if __name__ == "__main__":
    main()
