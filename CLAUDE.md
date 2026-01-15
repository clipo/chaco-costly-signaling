# Chaco Canyon Costly Signaling Project

## Project Overview

This project tests the costly signaling/bet-hedging framework on Chaco Canyon (850-1150 CE), examining whether investment in great houses and exotic goods represents multi-scale signaling under environmental uncertainty.

## Core Theoretical Framework

### Nested Selection Model

The model implements signaling at two scales simultaneously:

1. **Group Level (Great Houses)**
   - Monument construction as corporate group signal
   - Reduces inter-group conflict through deterrence
   - Attracts pilgrims/labor to the system
   - Cost: ~35% productivity diversion to construction

2. **Individual Level (Elites)**
   - Exotic goods (turquoise, macaws, cacao) as personal status signals
   - Competition for ritual authority within/across houses
   - Cost: Long-distance acquisition effort
   - Benefit: Marriage alliances, political position

### Environmental Parameters

Chaco Canyon environmental calibration (from paleoclimate data):
- **Shortfall frequency**: Variable, ENSO-driven (~7-15 year cycles)
- **Shortfall magnitude**: 0.3-0.6 (30-60% productivity reduction during drought)
- **Base productivity**: Low (marginal agricultural environment)
- **Carrying capacity**: ~1,000-3,000 (debated; pilgrimage vs. permanent residence)

## Key Archaeological Facts (Maintain Consistency)

### Chronology
- **Great house construction**: 850-1150 CE
- **Peak florescence**: 1020-1110 CE
- **Abandonment**: ~1130-1150 CE (coincides with megadrought)
- **Timber sourcing shift**: ~1020 CE (Zuni → Chuska Mountains)

### Great Houses
- **Pueblo Bonito**: Largest, 350+ ground-floor rooms, 32 kivas, construction 850-1125 CE
- **Chetro Ketl**: Second largest, unique colonnade, construction ~990-1115 CE
- **Total great houses in canyon**: ~12-15 major structures
- **Outlier great houses**: ~150 in broader region

### Exotic Goods
- **Scarlet macaws**: 35 recovered from canyon; imported from 900 CE (earlier than expected)
- **Turquoise**: 200,000+ pieces; nearest source 200+ km (Cerrillos Hills)
- **Cacao**: Documented at Pueblo Bonito
- **Marine shell, copper bells**: Long-distance trade items

### Population
- **Canyon estimates**: 2,000-3,000 at peak (debated)
- **Sustainable year-round**: Possibly only ~1,000 (Benson et al. 2019)
- **Regional (San Juan Basin)**: ~55,000
- **Pilgrimage model**: Seasonal population flux possible

### Violence/Conflict
- **During Chaco florescence**: Low evidence ("Pax Chaco")
- **Great houses**: NOT defensively sited
- **Post-Chaco (1150-1300 CE)**: High violence at Mesa Verde sites
- **Small House (~900 CE)**: Dismemberment evidence

## Data Sources

### Paleoclimate (PDSI)
- **Primary**: Cook et al. 2004 North American Drought Atlas
- **Access**: NOAA NCEI, Tree-Ring Drought Atlas Portal
- **Resolution**: Annual, gridded

### Construction Chronology
- **Primary**: Guiterman et al. 2015 PNAS (timber dating)
- **240,000+ timbers** dated dendrochronologically
- **Annual precision** for construction phases

### Exotic Goods Timing
- **Macaws**: Watson et al. 2015 PNAS (radiocarbon dating)
- **Turquoise**: Various sources (spatial distribution studies)

## Model Architecture

### Spatial Structure
```
Chaco Core (canyon)
├── Great House 1 (e.g., Pueblo Bonito)
│   ├── Elite agents (individual signaling)
│   └── Commoner agents (labor pool)
├── Great House 2 (e.g., Chetro Ketl)
│   └── ...
└── ...

Outlier Network
├── Outlier Community 1
│   └── Small great house (emulation)
├── Outlier Community 2
└── ...
```

### Signaling Channels

| Channel | Scale | Cost Parameter | Benefit Parameter |
|---------|-------|----------------|-------------------|
| Monuments | Group | C_monument = 0.35 | r_conflict = 0.75 |
| Exotics | Individual | C_acquisition = variable | status_benefit = variable |

## Testable Predictions

1. **Construction-PDSI correlation**: Negative (more building during drought)
2. **Exotic goods-stress correlation**: Positive (more acquisition during stress)
3. **Violence timing**: Low during florescence, high after collapse
4. **Abandonment**: Follows extreme prolonged drought

## File Naming Conventions

### Data Files
- `pdsi_chaco_[start_year]_[end_year].csv`
- `construction_chronology_[source].csv`
- `exotic_goods_dates_[type].csv`

### Figures
- `Figure_[N]_[description].png`
- Use descriptive names matching manuscript references

### Scripts
- `process_[data_type].py`
- `analyze_[analysis_type].py`
- `create_figure_[N]_[description].py`

## Manuscript Requirements

### Citation Style
- Author-year format (e.g., "Guiterman et al. 2015")
- Full author lists in bibliography
- All references must be verified real publications

### Figure Formatting
- PNG for raster, SVG for vector
- Colorblind-friendly palette
- Clear axis labels and legends

### Writing Style
- Narrative paragraphs (no bullet points in main text)
- No em-dashes or en-dashes
- Times New Roman 11pt for Word output

## Key References (Verified)

1. Guiterman, C.H., et al. 2015. Eleventh-century shift in timber procurement areas for the great houses of Chaco Canyon, NM. *PNAS* 112(44):13438-13443.

2. Watson, A.S., et al. 2015. Early procurement of scarlet macaws and the emergence of social complexity in Chaco Canyon, NM. *PNAS* 112(27):8238-8243.

3. Benson, L.V., et al. 2019. Prehistoric Chaco Canyon, New Mexico: Residential population implications of limited agricultural and mammal productivity. *Journal of Archaeological Science* 106:1-15.

4. Cook, E.R., et al. 2004. Long-term aridity changes in the western United States. *Science* 306(5698):1015-1018.

5. Lekson, S.H. (ed.) 2006. *The Archaeology of Chaco Canyon: An Eleventh-Century Pueblo Regional Center*. SAR Press.

6. Crown, P.L. 2018. Drinking Performance and Politics in Pueblo Bonito, Chaco Canyon. *American Antiquity* 83(3):387-406.

7. Mills, B.J., et al. 2013. Transformation of social networks in the late pre-Hispanic US Southwest. *PNAS* 110(15):5785-5790.

## Comparison with Rapa Nui Project

This is a **separate, independent project** that tests the same theoretical framework in a different context. Key differences:

| Feature | Rapa Nui | Chaco |
|---------|----------|-------|
| Signal types | Monuments only | Monuments + exotics |
| Selection scale | Group only | Group + individual |
| Population | Closed island | Open (pilgrimage) |
| Outcome | Persist until contact | Collapse ~1150 CE |
| Data resolution | Moderate | High (annual dendro) |
