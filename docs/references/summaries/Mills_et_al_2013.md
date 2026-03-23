# Summary: Mills et al. 2013

**Full citation**: Mills, B.J., Clark, J.J., Peeples, M.A., Haas, W.R. Jr., Roberts, J.M. Jr., Hill, J.B., Huntley, D.L., Borck, L., Breiger, R.L., Clauset, A. & Shackley, M.S. 2013. Transformation of social networks in the late pre-Hispanic US Southwest. *Proceedings of the National Academy of Sciences* 110(15):5785-5790. DOI: 10.1073/pnas.1219966110
**PDF filename**: Mills_et_al_2013.pdf
**Date summarized**: 2026-03-23
**Pipeline status**: index

---

## Relevance to Argument

This paper introduces the Southwest Social Networks (SWSN) database and provides the first comprehensive formal network analysis of the post-Chaco reorganization. The SWSN dataset is the empirical foundation for testing the model's Layer 3 predictions about cooperation networks. The paper's findings, particularly the weak correlation between spatial and social distance, the high mean tie distances (70-120 km), the north-to-south network shift after AD 1300, and the differential stability of large vs. small networks, all bear directly on the model's predictions about signaling-based network formation and network resilience.

## Key Claims

| Claim | Page | Type | Strength | Notes |
|-------|------|------|----------|-------|
| SWSN database: 4.3 million ceramics, 700+ sites, 4,800+ obsidian pieces, 334,000 km-sq | p. 5785 | empirical | strong | Foundational dataset |
| Dramatic north-to-south shift in network density and centrality after AD 1300 | p. 5785 | empirical | strong | Core finding |
| LCC shifted north to south; percentage of nodes in LCC grew from 25% to 51% | Table 2 | empirical | strong | Quantified transformation |
| Social distance does not track spatial distance; Pearson's r never exceeded 0.34 | pp. 5787-5788 | empirical | strong | Supports selective network formation |
| Mean weighted degree centrality: north stable (0.16-0.24), south increased 0.11 to 0.50 | Table 1 | empirical | strong | Divergent trajectories |
| Salado polychrome network emerged post-AD 1300, tying multi-valley settlements | pp. 5787-5788 | empirical | strong | New integrative tradition |
| Southern Salado communities were diverse/multiethnic; network promoted integration | p. 5789 | interpretive | moderate | Relevant to cooperation among strangers |
| Mean strong-tie distances: 70-120 km; long-distance ties exceeded 250 km | p. 5788 | empirical | strong | Costly network maintenance |
| Obsidian density increased 10-fold after AD 1300; raw material replaced finished tools | pp. 5788-5789 | empirical | strong | Exchange organization shift |
| Sites with overrepresented obsidian sources have higher ceramic similarity | p. 5789 | empirical | strong | Multi-material convergence |
| Large southern network collapsed; smaller northern networks (Hopi, Zuni) persisted | p. 5789 | empirical/interp | moderate | Network resilience finding |
| Ceramic assemblages reflect active signaling of social boundaries (among other mechanisms) | p. 5786 | methodological | strong | Explicit signaling acknowledgment |

## Data Presented

- **Table 1**: Mean weighted degree centrality by region and period (northern vs. southern SW, 5 intervals)
- **Table 2**: Topological properties: LCC size (%), number of connections (L), mean degree (k), average path length (p), diameter (D), LCC location
- **Figure 1**: Network graphs (Fruchterman-Reingold layout) for five 50-year intervals
- **Obsidian data**: 4,805 pieces from 11 geological sources, analyzed by XRF
- **Friction surface**: Cost-adjusted distance from 90 m SRTM DEM; 10 concentric 1-km buffer polygons

## Methodological Notes

- Ceramic networks based on Brainerd-Robinson similarity of decorated ware proportions, with 75% threshold for binarized network construction.
- Eigenvector centrality used as primary metric (accounts for indirect connections, not just immediate neighbors).
- Ceramic assemblages apportioned to five 50-year intervals using site occupation spans and ware production spans (method of Roberts et al.).
- Obsidian sourcing by XRF (Spectrace QuanX, Thermoscientific Quant'X, and portable EDXRF).
- Gravity model for expected obsidian source proportions based on terrain-cost-adjusted distances.
- Network graphs visualized in R using Fruchterman-Reingold force-directed algorithm.

## Connections to Other Sources

- **Foundational for**: Gauthier 2021 (uses SWSN v1.0 data); all subsequent SWSN-based analyses
- **Depends on**: Peeples and Haas 2013 (brokerage and social capital); Hill et al. 2015 (multiscalar perspectives)
- **Corroborates**: Gauthier 2021 (distance not sole predictor of interaction); Kantner & Vaughn 2012 (cooperation among diverse groups)
- **Extends**: Previous regional interaction studies by applying formal SNA at unprecedented scale
- **Relevant to**: Kohler et al. 2023 (network context for inequality dynamics)

## Verification Notes

- The PDF in the repository is a 1-page browser screenshot, not the full article. Content was verified via PMC (PMC3625298) full text extraction.
- Page numbers refer to PNAS published pagination (pp. 5785-5790).
