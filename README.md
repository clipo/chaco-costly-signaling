# Chaco Canyon Costly Signaling Project

An agent-based model and empirical analysis testing whether investment in great houses and long-distance exotic goods procurement at Chaco Canyon represents multi-scale costly signaling under environmental uncertainty.

## Overview

This project applies a costly signaling/bet-hedging framework to Chaco Canyon (850-1150 CE), exploring:

1. **Group-level signaling**: Great houses as corporate groups competing through monument construction
2. **Individual-level signaling**: Elites competing through exotic goods acquisition (turquoise, macaws, cacao)
3. **Environmental contingency**: Whether signaling investment correlates with drought stress

## Key Predictions

1. Construction intensifies during/after drought events (not surplus periods)
2. Exotic goods procurement increases during environmental stress
3. "Pax Chaco" - low violence during peak signaling, high after collapse (~1150 CE)
4. System collapse follows extreme prolonged drought (mid-12th century megadrought)

## Data Sources

### Paleoclimate
- North American Drought Atlas (Cook et al. 2004): 2000+ year PDSI reconstructions
- Tree-Ring Drought Atlas Portal: http://drought.memphis.edu/

### Archaeological
- Chaco Research Archive: https://www.chacoarchive.org/
- Dendrochronological construction dates (Guiterman et al. 2015 PNAS)
- Scarlet macaw dating (Watson et al. 2015 PNAS)

## Project Structure

```
chaco-signaling/
├── src/chaco/           # Python package for simulation and analysis
├── data/
│   ├── raw/             # Original data files
│   └── processed/       # Cleaned/formatted data
├── docs/manuscript/     # Paper draft and bibliography
├── figures/final/       # Publication-ready figures
├── scripts/             # Data processing and figure generation
└── tests/               # Unit tests
```

## Key References

1. Guiterman et al. 2015. Eleventh-century shift in timber procurement areas for the great houses of Chaco Canyon, NM. *PNAS* 112(44):13438-13443.

2. Watson et al. 2015. Early procurement of scarlet macaws and the emergence of social complexity in Chaco Canyon, NM. *PNAS* 112(27):8238-8243.

3. Benson et al. 2019. Prehistoric Chaco Canyon, New Mexico: Residential population implications of limited agricultural and mammal productivity. *JAS* 106:1-15.

4. Cook et al. 2004. Long-term aridity changes in the western United States. *Science* 306(5698):1015-1018.

5. Lekson (ed.) 2006. *The Archaeology of Chaco Canyon: An Eleventh-Century Pueblo Regional Center*. SAR Press.

## Related Work

This project applies the framework developed in the Rapa Nui costly signaling study (separate repository) to test generalizability across different cultural and environmental contexts.

## License

[To be determined]
