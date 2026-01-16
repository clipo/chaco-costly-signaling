#!/usr/bin/env python3
"""
Create Word document with embedded figures at first mention.

This script:
1. Reads the markdown manuscript
2. Identifies figure references in the text
3. Creates a Word document with figures inserted at first mention
4. Applies proper formatting per CLAUDE.md requirements
"""

from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.style import WD_STYLE_TYPE
import re


def get_project_root() -> Path:
    """Get project root directory."""
    return Path(__file__).parent.parent


def setup_styles(doc):
    """Set up document styles according to CLAUDE.md requirements."""
    # Get or create styles
    styles = doc.styles

    # Normal style - Times New Roman 11pt
    normal = styles['Normal']
    normal.font.name = 'Times New Roman'
    normal.font.size = Pt(11)

    # Heading 1 - Bold
    h1 = styles['Heading 1']
    h1.font.name = 'Times New Roman'
    h1.font.size = Pt(11)
    h1.font.bold = True
    h1.font.italic = False

    # Heading 2 - Italic
    h2 = styles['Heading 2']
    h2.font.name = 'Times New Roman'
    h2.font.size = Pt(11)
    h2.font.bold = False
    h2.font.italic = True

    # Heading 3 - Underlined
    h3 = styles['Heading 3']
    h3.font.name = 'Times New Roman'
    h3.font.size = Pt(11)
    h3.font.bold = False
    h3.font.italic = False
    h3.font.underline = True


def parse_markdown(md_path: Path) -> list:
    """
    Parse markdown into structured content blocks.

    Returns list of dicts with type and content.
    Stops at "Figure Legends" section to avoid duplicate captions.
    """
    with open(md_path, 'r') as f:
        content = f.read()

    blocks = []
    lines = content.split('\n')
    current_para = []

    for line in lines:
        # Stop processing at Figure Legends section to avoid duplicate captions
        if line.strip() == '## Figure Legends':
            if current_para:
                blocks.append({'type': 'paragraph', 'content': ' '.join(current_para)})
            break
        # Heading 1
        if line.startswith('# ') and not line.startswith('## '):
            if current_para:
                blocks.append({'type': 'paragraph', 'content': ' '.join(current_para)})
                current_para = []
            blocks.append({'type': 'heading1', 'content': line[2:].strip()})

        # Heading 2
        elif line.startswith('## '):
            if current_para:
                blocks.append({'type': 'paragraph', 'content': ' '.join(current_para)})
                current_para = []
            blocks.append({'type': 'heading2', 'content': line[3:].strip()})

        # Heading 3
        elif line.startswith('### '):
            if current_para:
                blocks.append({'type': 'paragraph', 'content': ' '.join(current_para)})
                current_para = []
            blocks.append({'type': 'heading3', 'content': line[4:].strip()})

        # Heading 4
        elif line.startswith('#### '):
            if current_para:
                blocks.append({'type': 'paragraph', 'content': ' '.join(current_para)})
                current_para = []
            blocks.append({'type': 'heading4', 'content': line[5:].strip()})

        # Empty line - end paragraph
        elif line.strip() == '':
            if current_para:
                blocks.append({'type': 'paragraph', 'content': ' '.join(current_para)})
                current_para = []

        # Regular text
        else:
            current_para.append(line.strip())

    # Don't forget last paragraph
    if current_para:
        blocks.append({'type': 'paragraph', 'content': ' '.join(current_para)})

    return blocks


def find_figure_references(text: str) -> list:
    """Find all figure references in text."""
    # Match patterns like "Figure 1", "Figure 2", etc.
    pattern = r'Figure\s+(\d+)'
    matches = re.findall(pattern, text)
    return [int(m) for m in matches]


def get_figure_path(fig_num: int, figures_dir: Path) -> Path:
    """Get the path to a figure file."""
    pattern = f"figure_{fig_num}_*.png"
    matches = list(figures_dir.glob(pattern))
    if matches:
        return matches[0]
    return None


def get_figure_caption(fig_num: int) -> str:
    """Get the caption for a figure."""
    captions = {
        1: "Figure 1. PMDI Time Series for Chaco Canyon Region (800-1200 CE). Annual Palmer Modified Drought Index values reconstructed from the Living Blended Drought Atlas v2 (NOAA). Shaded periods indicate major drought events. Vertical dashed lines mark key transitions: Chaco florescence onset (1000 CE) and megadrought/abandonment (1130 CE).",
        2: "Figure 2. Theoretical Framework and Predictions. Four-panel figure showing (A) dual signaling channel structure, (B) environmental uncertainty parameter phase space with Chaco periods marked, (C) theoretical predictions with expected directions, and (D) calculated σ values for different Chaco periods.",
        3: "Figure 3. Phase Space Predictions. Model predictions under different environmental conditions: (A) environmental phase space showing signaling dominance regions with Chaco periods marked, (B) predicted population trajectories for low, moderate, and extreme σ conditions, (C) signaling investment patterns showing intensification during stress, and (D) outcome summary by environmental condition.",
        4: "Figure 4. Drought Events Catalog. Visualization of all drought events identified in the PMDI reconstruction, showing timing, severity, and duration of each event.",
        5: "Figure 5. Construction-Climate Correlation Analysis. Scatter plot showing relationship between PMDI values and timber count (construction proxy) from dendrochronological data. Negative correlation indicates increased construction during drought conditions.",
        6: "Figure 6. Replicate Validation with Confidence Intervals. Four-panel figure showing simulation results across 100 replicates: (A) population by scenario, (B) signaling investment, (C) construction-climate correlation with 95% CI, and (D) exotic goods-stress correlation with 95% CI.",
        7: "Figure 7. Exotic Goods Chronology. Detailed analysis of exotic goods timing including (A) scarlet macaw imports, (B) turquoise accumulation, (C) all exotic goods by type, and (D) timing relative to severe droughts.",
        8: "Figure 8. Simulation Dynamics Overview. Four-panel figure showing (A) population trajectories, (B) monument accumulation, (C) exotic goods acquisition, and (D) conflict events across the 400-year simulation period.",
        9: "Figure 9. Period Comparison Statistics. Comparison of key metrics across four archaeological periods: Pre-Chaco (800-900 CE), Early Chaco (900-1000 CE), Peak Chaco (1000-1100 CE), and Late Chaco/Collapse (1100-1200 CE).",
        10: "Figure 10. Comprehensive Validation. Six-panel figure comparing model predictions to archaeological patterns: (A) construction chronology, (B) construction-climate scatter, (C) exotic goods timing, (D) population dynamics, (E) monument-productivity relationship, and (F) summary statistics table.",
    }
    return captions.get(fig_num, f"Figure {fig_num}.")


def add_figure(doc, fig_path: Path, caption: str):
    """Add a figure with caption to the document."""
    # Add the image
    para = doc.add_paragraph()
    para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = para.add_run()
    run.add_picture(str(fig_path), width=Inches(6))

    # Add caption (italic with bold first sentence)
    caption_para = doc.add_paragraph()
    caption_para.alignment = WD_ALIGN_PARAGRAPH.LEFT

    # Split caption into first sentence and rest
    parts = caption.split('. ', 1)
    if len(parts) == 2:
        # First sentence bold and italic
        run1 = caption_para.add_run(parts[0] + '. ')
        run1.font.name = 'Times New Roman'
        run1.font.size = Pt(11)
        run1.font.bold = True
        run1.font.italic = True

        # Rest just italic
        run2 = caption_para.add_run(parts[1])
        run2.font.name = 'Times New Roman'
        run2.font.size = Pt(11)
        run2.font.bold = False
        run2.font.italic = True
    else:
        run = caption_para.add_run(caption)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(11)
        run.font.italic = True

    # Add blank line after figure
    doc.add_paragraph()


def clean_markdown_formatting(text: str) -> list:
    """
    Convert markdown formatting to Word formatting instructions.

    Returns list of (text, is_bold, is_italic) tuples.
    """
    result = []

    # Handle bold+italic first (***)
    text = re.sub(r'\*\*\*([^*]+)\*\*\*', r'<<<BOLDITALIC>>>\1<<<ENDBOLDITALIC>>>', text)

    # Handle bold (**)
    text = re.sub(r'\*\*([^*]+)\*\*', r'<<<BOLD>>>\1<<<ENDBOLD>>>', text)

    # Handle italic (*)
    text = re.sub(r'\*([^*]+)\*', r'<<<ITALIC>>>\1<<<ENDITALIC>>>', text)

    # Split and process
    parts = re.split(r'(<<<[A-Z]+>>>)', text)

    is_bold = False
    is_italic = False

    for part in parts:
        if part == '<<<BOLD>>>':
            is_bold = True
        elif part == '<<<ENDBOLD>>>':
            is_bold = False
        elif part == '<<<ITALIC>>>':
            is_italic = True
        elif part == '<<<ENDITALIC>>>':
            is_italic = False
        elif part == '<<<BOLDITALIC>>>':
            is_bold = True
            is_italic = True
        elif part == '<<<ENDBOLDITALIC>>>':
            is_bold = False
            is_italic = False
        elif part:
            result.append((part, is_bold, is_italic))

    return result


def add_formatted_paragraph(doc, text: str, style: str = 'Normal'):
    """Add a paragraph with markdown formatting converted to Word formatting."""
    para = doc.add_paragraph(style=style)

    formatted_parts = clean_markdown_formatting(text)

    for part_text, is_bold, is_italic in formatted_parts:
        run = para.add_run(part_text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(11)
        run.font.bold = is_bold
        run.font.italic = is_italic

    return para


def create_word_document(md_path: Path, output_path: Path, figures_dir: Path):
    """Create Word document with embedded figures."""

    doc = Document()
    setup_styles(doc)

    blocks = parse_markdown(md_path)
    figures_inserted = set()

    for block in blocks:
        block_type = block['type']
        content = block['content']

        # Add the content block FIRST
        if block_type == 'heading1':
            para = doc.add_paragraph(content, style='Heading 1')
        elif block_type == 'heading2':
            para = doc.add_paragraph(content, style='Heading 2')
        elif block_type == 'heading3':
            para = doc.add_paragraph(content, style='Heading 3')
        elif block_type == 'heading4':
            para = doc.add_paragraph(content, style='Normal')
            for run in para.runs:
                run.bold = False
        elif block_type == 'paragraph':
            if content.strip():
                add_formatted_paragraph(doc, content)

        # Check for figure references AFTER adding content (insert figure after paragraph)
        if block_type == 'paragraph':
            fig_refs = find_figure_references(content)

            for fig_num in fig_refs:
                if fig_num not in figures_inserted:
                    fig_path = get_figure_path(fig_num, figures_dir)
                    if fig_path and fig_path.exists():
                        caption = get_figure_caption(fig_num)
                        add_figure(doc, fig_path, caption)
                        figures_inserted.add(fig_num)
                        print(f"  Inserted Figure {fig_num}")

    # Save document
    doc.save(str(output_path))
    print(f"\nSaved: {output_path}")
    print(f"Total figures inserted: {len(figures_inserted)}")


def main():
    root = get_project_root()

    md_path = root / 'docs' / 'manuscript' / 'Chaco_Signaling_Manuscript.md'
    output_path = root / 'docs' / 'manuscript' / 'Chaco_Signaling_Manuscript.docx'
    figures_dir = root / 'figures' / 'final'

    print("Creating Word document with embedded figures...")
    print(f"  Source: {md_path}")
    print(f"  Output: {output_path}")
    print(f"  Figures: {figures_dir}")
    print()

    create_word_document(md_path, output_path, figures_dir)

    print("\nDocument creation complete!")


if __name__ == '__main__':
    main()
