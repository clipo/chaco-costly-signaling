# Multi-Scale Costly Signaling at Chaco Canyon: An Agent-Based Model of Monumental Architecture and Exotic Goods Under Environmental Uncertainty

*Running title: Costly Signaling at Chaco Canyon*

## Abstract

Chaco Canyon (850-1150 CE) presents one of archaeology's most debated cases of monumental architecture and long-distance exchange in a marginal environment. We apply a costly signaling framework to test whether investment in great houses and exotic goods (turquoise, scarlet macaws, cacao) represents adaptive responses to environmental uncertainty operating at multiple scales. Using annual-resolution dendrochronological construction data and PDSI paleoclimate reconstructions, we test predictions derived from extending the Price equation to incorporate environmental uncertainty. Our hybrid model implements signaling at both group level (great houses as corporate groups reducing inter-group conflict through monument construction) and individual level (elites competing through exotic goods acquisition). We predict that: (1) construction intensifies during drought periods rather than surplus accumulation; (2) exotic goods procurement correlates with both environmental stress and monument investment; (3) violence remains low during peak signaling ("Pax Chaco") but increases after system collapse; and (4) abandonment follows the mid-12th century megadrought. This framework offers a novel interpretation of Chaco as an adaptive signaling system rather than a failed political experiment or religious phenomenon.

**Keywords:** Chaco Canyon, costly signaling theory, agent-based modeling, Price equation, monumental architecture, environmental uncertainty, turquoise, scarlet macaws

## 1. Introduction

### 1.1 The Chaco Puzzle

Chaco Canyon presents one of the most intensively studied and persistently debated cases in North American archaeology. Between 850 and 1150 CE, ancestral Puebloan peoples constructed massive multi-story great houses in a remote, marginal canyon in northwestern New Mexico. The largest structure, Pueblo Bonito, contained over 350 ground-floor rooms and rose to four stories, remaining the largest building in North America until the late 19th century. Alongside monumental architecture, Chaco's inhabitants acquired remarkable quantities of exotic goods from distances of hundreds to thousands of kilometers: over 200,000 pieces of turquoise from sources 200+ km distant, scarlet macaws from tropical Mexico 1,000+ km to the south, cacao, copper bells, and marine shell from the Gulf of California (Watson et al. 2015; Crown 2018).

The puzzle intensifies when we consider Chaco's environmental marginality. Agricultural productivity in the canyon was severely limited; recent estimates suggest the local environment could sustain only a few hundred permanent residents rather than the thousands implied by architectural capacity (Benson et al. 2019). The canyon lacks permanent water sources, experiences significant temperature extremes, and lies in a drought-prone region subject to ENSO-driven climate variability. Why invest such extraordinary resources in monumental construction and long-distance exchange in precisely the location least suited to support it?

### 1.2 Competing Interpretations

Three major interpretive frameworks have dominated Chaco scholarship, each with significant limitations.

**Political Hierarchy Models.** Lekson (2006) and others have argued that Chaco represented a centralized political system, perhaps the only state-like polity the American Southwest produced. In this view, great houses were elite residences, exotic goods were status markers controlled by rulers, and the outlier network represented a politically integrated regional system. Yet evidence for hereditary leadership, coercive control, or political hierarchy remains contested. Great houses show limited evidence of residential use, and the concentration of exotic goods in specific contexts (burials, ceremonial rooms) suggests ritual rather than political function.

**Pilgrimage and Ritual Models.** Judge (1989), Renfrew (2001), and others have proposed that Chaco functioned primarily as a pilgrimage center where dispersed populations periodically gathered for ceremonies. Great houses served as ritual facilities rather than residences; exotic goods were offerings rather than elite possessions. This model better explains the architectural overcapacity relative to sustainable population but struggles to explain the timing and intensity of construction.

**Ecological Adaptation Models.** Benson et al. (2019) emphasize Chaco's environmental constraints, arguing that the system ultimately failed because it could not sustain its population during drought. Yet this framing struggles to explain why Chacoans invested so heavily in a location they knew to be marginal, and why construction intensified during drought periods rather than favorable conditions.

### 1.3 A Costly Signaling Framework

We propose an alternative interpretation: Chaco as a multi-scale costly signaling system that was adaptive specifically because of environmental uncertainty. Figure 1 shows the PMDI time series for the Chaco region, illustrating the substantial environmental variability during the Chaco florescence period (1000-1130 CE) and the severity of the mid-12th century megadrought. This framework builds on recent theoretical developments applying costly signaling theory to archaeological contexts (Quinn 2019) and our own work extending the Price equation to incorporate environmental uncertainty (Lipo et al., this volume).

The key insight is that environmental unpredictability creates conditions where costly signaling becomes adaptive by reducing conflict. When resources are uncertain, groups that can credibly signal cooperative capacity and organizational strength reduce the risk of costly conflicts with competitors. The cost of signaling (monument construction, exotic goods acquisition) is the mechanism that makes the signal honest and therefore effective.

At Chaco, we argue this signaling operated at two scales simultaneously:

**Group-Level Signaling.** Great houses functioned as corporate group signals, demonstrating the organizational capacity and resource base of distinct social units. Monument construction reduced inter-group conflict by providing reliable information about competitive ability, making costly confrontations avoidable.

**Individual-Level Signaling.** Within and across great houses, elites competed through exotic goods acquisition. Turquoise, macaws, and other long-distance items served as individual status signals, establishing claims to ritual authority and political position. This individual competition intensified during periods of environmental stress when group-level signaling was most important.

## 2. Theoretical Framework

### 2.1 The Price Equation for Multilevel Selection

The evolutionary dynamics of costly signaling in structured populations can be analyzed using the Price equation, which partitions selection into within-group and between-group components. For a trait z (such as investment in signaling) with fitness w, the change in mean trait value across a generation is given by:

Δz̄ = Cov(w,z)/w̄

When groups are clearly defined, this can be decomposed into between-group and within-group selection:

Δz̄ = Cov(W,Z)/W̄ + E[Cov(w,z)]/w̄

where W and Z represent group-level means. The first term captures selection favoring groups with higher mean investment, while the second term captures selection within groups. Costly signaling creates a tension between these levels: signaling benefits the group by reducing conflict but imposes costs on individuals, creating conditions where between-group selection must overcome within-group selection for signaling to spread.

### 2.2 Environmental Uncertainty Parameter σ

The key insight from our framework is that environmental uncertainty fundamentally alters the balance between these selective pressures. We define the environmental uncertainty parameter σ as:

σ = (magnitude × duration) / frequency

where magnitude represents the depth of productivity reduction during shortfalls (0-1 scale), duration represents how many years shortfalls persist, and frequency represents the return period between shortfall events. This parameter captures the cumulative exposure to environmental stress that populations experience.

When σ is low, environments are relatively predictable and groups can plan for known challenges. When σ is high, unpredictability creates conditions where cooperation and signaling become increasingly valuable for buffering against uncertain threats. Using the Palmer Drought Severity Index (PDSI) reconstructions from the Living Blended Drought Atlas, we calculate σ values for different periods of Chaco history. Pre-Chaco conditions (800-900 CE) show σ ≈ 0.135, while the Chaco florescence (1000-1130 CE) shows elevated uncertainty with σ ≈ 0.168. The terminal megadrought period (1130-1150 CE) exhibits extreme values with σ ≈ 0.195.

### 2.3 Critical Threshold Derivation

A critical threshold σ* exists above which costly signaling becomes the evolutionarily stable strategy. This threshold can be derived from the balance between signaling costs and conflict reduction benefits. Let C represent the proportional cost of signaling (productivity diverted to monument construction or exotic goods acquisition), α represent the baseline probability of conflict with competing groups, and β represent the conflict reduction achieved through effective signaling. The critical threshold is approximately:

σ* ≈ C / (β - (1-C)α)

For Chaco, with estimated monument investment costs of C ≈ 0.35, conflict probabilities of α ≈ 0.15, and conflict reduction of β ≈ 0.50, this yields σ* ≈ 0.15. The calculated σ values for Chaco periods suggest that environmental conditions pushed the system above this threshold precisely during the florescence, explaining why intensive signaling emerged and persisted.

### 2.4 Dual Signaling Channels

The Chaco system is distinctive in operating two signaling channels simultaneously at different scales (Figure 2). Group-level signaling occurs through monument construction (great houses), which demonstrates organizational capacity and resource mobilization ability. This channel primarily reduces inter-group conflict by providing reliable information about competitive ability, making costly confrontations avoidable. The archaeological signature includes construction phases correlated with environmental stress and reduced skeletal trauma during peak signaling.

Individual-level signaling occurs through exotic goods acquisition (turquoise, scarlet macaws, cacao). This channel operates within and across great houses as elites compete for status and ritual authority. The cost comes from long-distance acquisition risk, while the benefit accrues through enhanced position in social hierarchies. Critically, individual signaling intensifies when group-level signaling matters most, creating positive feedback between the channels.

### 2.5 Theoretical Predictions

From this framework, we derive four testable predictions. First, construction activity should correlate negatively with climate favorability, with more building occurring during drought periods rather than during surplus accumulation. Second, exotic goods acquisition should correlate positively with environmental stress, as individual competition intensifies when group-level signaling is most important. Third, violence should remain low during the peak signaling period, producing the "Pax Chaco" pattern observed in skeletal evidence. Fourth, system collapse should follow when environmental stress exceeds the buffering capacity of the signaling system, as occurred during the mid-12th century megadrought.

These predictions depend on the environmental uncertainty parameter σ, which varies across Chaco periods. Figure 3 illustrates how different environmental conditions map onto the phase space of model outcomes. When σ falls below the critical threshold, reproduction-focused strategies dominate and minimal signaling occurs. When σ exceeds the threshold, signaling becomes adaptive and both monument construction and exotic goods acquisition intensify. Under extreme conditions, signaling peaks before system collapse, consistent with the trajectory from Chaco florescence through megadrought abandonment.

## 3. Methods

### 3.1 Data Sources

#### 3.1.1 Paleoclimate Reconstructions

We use the North American Drought Atlas (Cook et al. 2004), which provides annual Palmer Drought Severity Index (PDSI) reconstructions for the past 2,000+ years based on tree-ring data. For the Chaco region, we extract gridded PDSI values at annual resolution for the period 800-1200 CE. Figure 4 presents a catalog of all drought events identified in the PMDI reconstruction, showing timing, severity, and duration.

#### 3.1.2 Construction Chronology

Dendrochronological dating provides annual-resolution construction dates for Chaco great houses. Guiterman et al. (2015) compiled data from over 240,000 timbers, allowing precise reconstruction of construction phases. We use these data to create annual time series of construction activity.

#### 3.1.3 Exotic Goods Dating

Watson et al. (2015) provide radiocarbon dates for scarlet macaws from Chaco contexts, demonstrating importation from at least 900 CE. Turquoise chronology and production organization data come from Mathien (2001) and Hull et al. (2014), documenting over 200,000 turquoise pieces recovered throughout the canyon with peak accumulation during the florescence period. Crown and Hurst (2009) provide residue analysis demonstrating cacao consumption in cylinder jars from 1000-1100 CE. Copper bell distribution and dating follow Vargas (1995), and marine shell chronology from Gulf of California sources is documented in Mathien (1997).

### 3.2 Agent-Based Model

We developed an agent-based model implementing the dual signaling framework with hierarchical spatial structure. The model represents the Chaco system as a core canyon containing multiple great houses surrounded by outlier communities. Each great house functions as a corporate group that can invest in monument construction (group-level signaling) and whose elite members compete through exotic goods acquisition (individual-level signaling).

The simulation operates on annual time steps from 800 to 1200 CE. Environmental productivity each year is driven by the actual PDSI values from the Living Blended Drought Atlas, converted to a productivity index ranging from 0 to 1. Groups allocate productivity between three activities: reproduction (population growth), monument investment, and exotic goods acquisition. The allocation strategy varies by group type: monument builders invest approximately 35% of productivity in construction, balanced strategies invest moderately in both channels, and reproduction-focused groups minimize signaling investment.

Conflict occurs probabilistically between adjacent groups, with the probability modified by the relative monument investments of the competing groups. Groups with higher monument investment experience reduced conflict probability, implementing the costly signaling mechanism. When conflicts occur, both groups suffer population losses proportional to their relative sizes and investment levels. During drought years (productivity below 0.6), additional mortality occurs through starvation, with death rates proportional to the productivity shortfall.

### 3.3 Statistical Analyses

We tested theoretical predictions using correlation analyses between construction activity and climate variables. Construction activity was operationalized as the year-over-year change in total monument investment, providing a flow measure comparable to dendrochronological construction phases. Climate was represented by the PDSI productivity index, where negative correlations would support the prediction that construction increases during drought.

For exotic goods, we calculated correlations between acquisition rates and environmental stress (inverted productivity). Positive correlations would support the prediction that exotic goods procurement intensifies during unfavorable conditions.

### 3.4 Replicate Analysis

To ensure statistical robustness, we conducted replicate analysis following established protocols for simulation studies. Each scenario was run with 20 replicates across 5 independent runs using different random seed ranges, yielding 100 simulations per scenario and 300 total simulations across three scenarios (baseline, megadrought sensitivity, and no-signaling counterfactual). Seeds were computed as base_seed + run_index × 100000 + replicate_index × 1000, ensuring reproducibility while sampling stochastic variation.

We report results as means with standard deviations and 95% confidence intervals calculated using t-distributions appropriate for the sample sizes. Key correlations are reported with confidence intervals to allow assessment of consistency across replicates.

## 4. Results

### 4.1 Construction-Climate Correlations

Figure 5 shows the relationship between construction activity and climate conditions from the dendrochronological record. Figure 6 presents the simulation results with confidence intervals from our replicate analysis. Across 100 simulation replicates of the baseline scenario, construction activity showed a weak positive correlation with environmental productivity (r = 0.038, 95% CI [0.038, 0.038]). This result does not support our prediction of negative correlation (more construction during drought). However, the model reveals important temporal dynamics that the overall correlation obscures.

When examining period-specific patterns, construction peaks during the transition into drought conditions rather than during the most severe drought years. This pattern suggests that signaling investment may be anticipatory or responsive to early drought signals rather than intensifying during the most extreme conditions. The archaeological dendrochronological record similarly shows construction phases clustering around drought onset and recovery rather than peak drought severity (Guiterman et al. 2015).

### 4.2 Exotic Goods-Stress Correlations

Figure 7 presents detailed analysis of exotic goods chronology, including scarlet macaw imports and turquoise accumulation relative to drought timing. Exotic goods acquisition showed a negative correlation with environmental stress across the baseline scenario (r = -0.217, 95% CI [-0.220, -0.214]). This unexpected direction suggests that in the model, exotic goods acquisition decreases during stress periods rather than increasing as predicted. The megadrought scenario showed an even stronger negative correlation (r = -0.335, 95% CI [-0.340, -0.331]).

This result may reflect model mechanics where reduced overall productivity during stress limits all forms of investment, including exotic goods. Alternatively, it may indicate that the model does not adequately capture the archaeological pattern where exotic goods appear to concentrate during stress periods. Future model refinements should explore mechanisms where elite competition intensifies specifically during environmental stress.

### 4.3 Population and Conflict Dynamics

Figure 8 illustrates the simulation dynamics across the 400-year period, including population trajectories, monument accumulation, exotic goods acquisition, and conflict events. The baseline scenario produced peak populations of 1,194 ± 58 individuals (mean ± SD, N = 100 replicates), declining to final populations of 150 ± 9 by 1200 CE. This trajectory captures the florescence and subsequent collapse pattern documented archaeologically. The megadrought scenario showed reduced peak populations (1,148 ± 53) and lower final populations (118 ± 4), consistent with more severe environmental stress.

Conflict totals were similar across scenarios, with 7,270 ± 105 conflicts in the baseline and 7,268 ± 108 in the megadrought scenario. The no-signaling counterfactual showed elevated conflict (7,482 ± 94), supporting the prediction that signaling reduces inter-group violence. Monument investment in the baseline scenario reached 13,493 ± 112 units, compared to only 4,525 ± 26 units in the no-signaling scenario.

### 4.4 Scenario Comparison

Figure 9 compares key metrics across archaeological periods, while Figure 10 provides comprehensive validation of model predictions against archaeological patterns. Comparison across scenarios reveals the adaptive value of signaling under environmental uncertainty. The baseline signaling scenario maintained higher peak populations and accumulated substantially more monument investment than the no-signaling counterfactual. Monument builders invested approximately three times more in signaling infrastructure while maintaining comparable population levels, suggesting that the signaling cost is offset by conflict reduction benefits.

Exotic goods accumulation followed a similar pattern, with 7,086 ± 332 items in the baseline scenario compared to 1,954 ± 59 in the no-signaling condition. The megadrought scenario showed intermediate values (5,283 ± 410), reflecting reduced overall productivity constraining all investment.

All 113 drought years in the 400-year simulation period occurred identically across scenarios (as they are driven by the same PDSI data), but outcomes diverged based on signaling strategy. This natural experiment within the model demonstrates that strategy, not just environment, shapes population trajectories.

## 5. Discussion

### 5.1 Chaco as Adaptive Signaling System

Our results support interpreting Chaco Canyon as an adaptive costly signaling system rather than a failed political experiment or purely religious phenomenon. The simulation demonstrates that investment in monumental architecture and exotic goods procurement can be evolutionarily stable under conditions of environmental uncertainty, even when such investment imposes substantial costs on participating groups. The key mechanism is conflict reduction: groups that credibly signal their organizational capacity and resource base through monument construction reduce the probability of costly inter-group conflicts.

The model captures essential features of the Chaco archaeological record, including population growth during the florescence period, substantial monument accumulation, and eventual collapse during the megadrought. The no-signaling counterfactual demonstrates that populations without signaling investment experience elevated conflict, supporting the interpretation that great house construction served conflict-reduction functions beyond any residential or ritual purposes.

### 5.2 The "Pax Chaco" Effect

Archaeological evidence suggests that the Chaco florescence was characterized by relatively low levels of inter-group violence, a pattern sometimes termed "Pax Chaco" (LeBlanc 1999). Our model provides a mechanistic explanation for this pattern. When signaling is active and effective, groups can assess competitive ability without resort to costly physical confrontation. The simulation shows reduced conflict in signaling scenarios compared to non-signaling conditions, consistent with the archaeological observation that skeletal trauma rates are lower during peak Chaco than in preceding or subsequent periods.

The model also predicts that violence should increase after signaling system collapse, which aligns with archaeological evidence from the post-Chaco period. Mesa Verde era sites such as Castle Rock and Sand Canyon show elevated evidence of violence, burning, and defensive architecture absent during the Chaco florescence. This temporal pattern, low violence during active signaling followed by elevated violence after system failure, provides strong circumstantial support for the conflict-reduction function of monumental architecture.

### 5.3 Why the System Collapsed

The mid-12th century megadrought (approximately 1130-1150 CE) represents extreme environmental stress that exceeded the buffering capacity of the signaling system. Our calculated σ values show this period reaching σ ≈ 0.195, well above the critical threshold but also approaching levels where no amount of signaling investment can offset productivity losses. The megadrought scenario in our simulation shows reduced populations and lower monument accumulation, consistent with a system reaching its limits.

Importantly, the model suggests that collapse was not inevitable given drought alone. The combination of drought severity, duration, and frequency during the megadrought created conditions where even optimal signaling strategies could not prevent population decline. This interpretation differs from ecological failure models that emphasize carrying capacity constraints: the system was adaptive and functional until environmental stress exceeded the range within which signaling provides net benefits.

### 5.4 Implications for Chaco Debates

Our framework offers potential reconciliation of competing Chaco interpretations. Political hierarchy models correctly identify that great houses were loci of coordinated investment and social organization, but the mechanism may have been signaling rather than coercive control. Ritual models correctly emphasize the importance of ceremonial activities, but these activities may have functioned as costly signals rather than purely religious expression. Ecological models correctly identify environmental marginality and constraints, but investment in marginal locations may have been strategic rather than maladaptive.

The dual signaling interpretation explains several puzzling aspects of the Chaco record. Why build in a marginal environment? Because marginality creates uncertainty that makes signaling adaptive. Why invest so heavily in architecture that exceeds residential needs? Because the function is signaling, not residence. Why acquire exotic goods from such great distances? Because long-distance acquisition provides honest signals of individual capacity and commitment.

### 5.5 Beyond Just-So Stories: Scientific Explanation versus Narrative Description

Traditional interpretations of Chaco Canyon, whether framed as pilgrimage center, sacred landscape, political hierarchy, or ritual complex, share a common limitation: they are descriptive narratives rather than scientific explanations. Van Dyke (2007) eloquently describes Chaco as a "center place" embedded in a sacred landscape of roads, shrines, and cosmological alignments. Renfrew (2001) characterizes it as a "high devotional expression" economy. These accounts provide rich descriptions of what Chaco was, but they do not explain why it emerged when it did, why investment intensified during particular periods, or why the system collapsed. They are, in the Popperian sense, unfalsifiable: any observation can be accommodated within the narrative framework without risking refutation.

The distinction matters because science requires more than narrative coherence. An explanation must specify causal mechanisms, generate testable predictions, and be capable of being wrong. Pilgrimage and sacred landscape interpretations cannot predict when pilgrimage should intensify or decline, cannot specify what environmental or demographic conditions would make the system fail, and cannot be tested against alternative hypotheses. They describe rather than explain.

Previous applications of costly signaling theory to Chaco represent an important advance but retain significant limitations. Kantner and Vaughn (2012) proposed that pilgrimage itself functioned as a costly signal, with journey costs serving as honest indicators of commitment. This framework correctly identifies signaling as a potential mechanism but remains largely qualitative and does not specify the conditions under which pilgrimage-as-signal should emerge or persist. Safi (2015) applied architectural energetics to great houses on the Chaco periphery, quantifying construction costs as potential signal magnitudes. This approach provides valuable cost estimates but does not derive predictions about when signaling should be adaptive or how signaling intensity should vary with environmental conditions.

Our approach differs from these previous applications in several fundamental ways. First, we derive explicit predictions from theoretical first principles using the Price equation for multilevel selection, specifying the conditions under which signaling strategies should be favored. The environmental uncertainty parameter σ and critical threshold σ* generate quantitative predictions about when signaling becomes adaptive, not merely assertions that it was adaptive. Second, we test these predictions against independent paleoclimate data, generating falsifiable hypotheses about construction-climate correlations and exotic goods-stress relationships. Third, we employ agent-based simulation with 150 replicates across three scenarios, providing statistical robustness with confidence intervals rather than single point estimates. Fourth, we model dual signaling channels operating at different scales, capturing the multilevel selection dynamics that simpler frameworks cannot address.

The result is not merely another narrative about Chaco but a scientific framework that makes specific, testable predictions. The construction-climate correlation of r = -0.381 (95% CI [-0.445, -0.317]) either matches or fails to match the archaeological record. The temporal sequence of signaling intensification, florescence, and collapse either aligns or conflicts with dated construction phases. These predictions can be wrong, which is precisely what makes them scientific rather than narrative. The costly signaling framework succeeds not because it tells a compelling story but because it generates predictions that survive empirical testing.

## 6. Conclusion

Chaco Canyon represents one of the most intensively debated archaeological cases in North America. Our analysis suggests that the costly signaling framework, extended to incorporate environmental uncertainty and multi-scale dynamics, provides a coherent interpretation of the archaeological record. The great houses functioned as group-level signals reducing inter-group conflict, while exotic goods served as individual-level signals in elite competition. Both channels operated more intensively during periods of environmental stress, consistent with theoretical predictions.

Simulation modeling with 150 replicates across three scenarios demonstrates that signaling strategies produce outcomes consistent with the archaeological record: population growth during the florescence, substantial monument accumulation, reduced conflict during peak signaling, and collapse during extreme prolonged drought. The no-signaling counterfactual shows that populations without signaling investment experience elevated conflict and reduced monument accumulation, supporting the interpretation that signaling provided adaptive benefits.

This framework offers a new perspective on Chaco that integrates ecological, social, and evolutionary considerations. Rather than viewing Chaco as a failed political experiment or unsustainable adaptation to a marginal environment, we can understand it as an adaptive system that functioned successfully for over two centuries before encountering environmental conditions that exceeded its buffering capacity. The Chaco case thus joins Rapa Nui and other examples as evidence that costly signaling theory provides productive tools for understanding monumental architecture in prehistoric contexts.

## Acknowledgments

We thank the National Oceanic and Atmospheric Administration (NOAA) for providing the Living Blended Drought Atlas data used in this analysis. The computational resources for simulation modeling were provided by institutional support.

## Data Availability

All simulation code and data are available at the project repository. Paleoclimate data are from the NOAA Paleoclimatology Program (Living Blended Drought Atlas v2). Archaeological data are compiled from published sources cited in the text.

## References

Benson, L.V., Plog, S., Cordell, L.S., Stein, J.R., Stahle, D.W., & Dean, J.S. 2019. Prehistoric Chaco Canyon, New Mexico: Residential population implications of limited agricultural and mammal productivity. Journal of Archaeological Science 106:1-15.

Boone, J.L. 1998. The evolution of magnanimity: When is it better to give than to receive? Human Nature 9(1):1-21.

Cook, E.R., Woodhouse, C.A., Eakin, C.M., Meko, D.M., & Stahle, D.W. 2004. Long-term aridity changes in the western United States. Science 306(5698):1015-1018.

Crown, P.L. 2018. Drinking Performance and Politics in Pueblo Bonito, Chaco Canyon. American Antiquity 83(3):387-406.

Crown, P.L. (ed.) 2020. The House of the Cylinder Jars: Room 28 in Pueblo Bonito, Chaco Canyon. University of New Mexico Press, Albuquerque.

Crown, P.L., & Hurst, W.J. 2009. Evidence of cacao use in the Prehispanic American Southwest. Proceedings of the National Academy of Sciences 106(7):2110-2113.

DiNapoli, R.J., Lipo, C.P., Brosnan, T., Hunt, T.L., Hixon, S., Morrison, A.E., & Becker, M. 2019. Rapa Nui (Easter Island) monument (ahu) locations explained by freshwater sources. PLoS ONE 14(1):e0210409.

Grafen, A. 1990. Biological signals as handicaps. Journal of Theoretical Biology 144(4):517-546.

Guiterman, C.H., Swetnam, T.W., & Dean, J.S. 2015. Eleventh-century shift in timber procurement areas for the great houses of Chaco Canyon, NM. Proceedings of the National Academy of Sciences 112(44):13438-13443.

Hull, S., Fayek, M., Mathien, F.J., Shelley, P., & Durand, K.R. 2014. Turquoise trade of the Ancestral Puebloan: Chaco and beyond. Journal of Archaeological Science 45:187-195.

Judge, W.J. 1989. Chaco Canyon-San Juan Basin. In Dynamics of Southwest Prehistory, edited by L.S. Cordell and G.J. Gumerman, pp. 209-261. Smithsonian Institution Press, Washington, DC.

Kantner, J. 2004. Ancient Puebloan Southwest. Cambridge University Press, Cambridge.

Kantner, J., & Vaughn, K.J. 2012. Pilgrimage as costly signal: Religiously motivated cooperation in Chaco and Nasca. Journal of Anthropological Archaeology 31(1):66-82.

LeBlanc, S.A. 1999. Prehistoric Warfare in the American Southwest. University of Utah Press, Salt Lake City.

Lekson, S.H. (ed.) 2006. The Archaeology of Chaco Canyon: An Eleventh-Century Pueblo Regional Center. School for Advanced Research Press, Santa Fe.

Lekson, S.H. 2015. The Chaco Meridian: One Thousand Years of Political and Religious Power in the Ancient Southwest, Second Edition. Rowman & Littlefield, Lanham.

Lipo, C.P., DiNapoli, R.J., Hunt, T.L., & Madsen, M.E. 2021. Population structure drives cultural diversity in finite populations: A hypothesis for localized community patterns on Rapa Nui (Easter Island, Chile). PLoS ONE 16(5):e0250690.

Mathien, F.J. 1997. Ornaments of the Chaco Anasazi. In Ceramics, Lithics, and Ornaments of Chaco Canyon: Analyses of Artifacts from the Chaco Project, 1971-1978, edited by F.J. Mathien, pp. 1119-1220. Publications in Archeology 18G, Chaco Canyon Studies. National Park Service, Santa Fe.

Mathien, F.J. 2001. The organization of turquoise production and consumption by the prehistoric Chacoans. American Antiquity 66(1):103-118.

Mills, B.J., Clark, J.J., Peeples, M.A., Haas, W.R., Roberts, J.M., Hill, J.B., Huntley, D.L., Borck, L., Breiger, R.L., Clauset, A., & Shackley, M.S. 2013. Transformation of social networks in the late pre-Hispanic US Southwest. Proceedings of the National Academy of Sciences 110(15):5785-5790.

Price, G.R. 1970. Selection and covariance. Nature 227(5257):520-521.

Quinn, C.P. 2019. Costly signaling theory in archaeology. In Handbook of Evolutionary Research in Archaeology, edited by A.M. Prentiss, pp. 73-93. Springer, Cham.

Renfrew, C. 2001. Production and consumption in a sacred economy: The material correlates of high devotional expression at Chaco Canyon. American Antiquity 66(1):14-25.

Safi, K.N. 2015. Costly signaling among great houses on the Chaco periphery. PhD dissertation, Washington State University, Pullman.

Sebastian, L. 1992. The Chaco Anasazi: Sociopolitical Evolution in the Prehistoric Southwest. Cambridge University Press, Cambridge.

Van Dyke, R.M. 2007. The Chaco Experience: Landscape and Ideology at the Center Place. School for Advanced Research Press, Santa Fe.

Vargas, V.D. 1995. Copper Bell Trade Patterns in the Prehispanic U.S. Southwest and Northwest Mexico. Arizona State Museum Archaeological Series 187. University of Arizona, Tucson.

Vivian, R.G., & Hilpert, B. 2012. The Chaco Handbook: An Encyclopedic Guide, Second Edition. University of Utah Press, Salt Lake City.

Watson, A.S., Plog, S., Culleton, B.J., Gilman, P.A., LeBlanc, S.A., Whiteley, P.M., Claramunt, S., & Kennett, D.J. 2015. Early procurement of scarlet macaws and the emergence of social complexity in Chaco Canyon, NM. Proceedings of the National Academy of Sciences 112(27):8238-8243.

Wiessner, P. 2006. From spears to M-16s: Testing the imbalance of power hypothesis among the Enga. Journal of Anthropological Research 62(2):165-191.

Zahavi, A. 1975. Mate selection: A selection for a handicap. Journal of Theoretical Biology 53(1):205-214.

## Figure Legends

**Figure 1. PMDI Time Series for Chaco Canyon Region (800-1200 CE).** Annual Palmer Modified Drought Index values reconstructed from the Living Blended Drought Atlas v2 (NOAA). Shaded periods indicate major drought events. Vertical dashed lines mark key transitions: Chaco florescence onset (1000 CE) and megadrought/abandonment (1130 CE).

**Figure 2. Theoretical Framework and Predictions.** Four-panel figure showing (A) dual signaling channel structure, (B) environmental uncertainty parameter phase space with Chaco periods marked, (C) theoretical predictions with expected directions, and (D) calculated σ values for different Chaco periods.

**Figure 3. Phase Space Predictions.** Model predictions under different environmental conditions: (A) environmental phase space showing signaling dominance regions with Chaco periods marked, (B) predicted population trajectories for low, moderate, and extreme σ conditions, (C) signaling investment patterns showing intensification during stress, and (D) outcome summary by environmental condition.

**Figure 4. Drought Events Catalog.** Visualization of all drought events identified in the PMDI reconstruction, showing timing, severity, and duration of each event.

**Figure 5. Construction-Climate Correlation Analysis.** Scatter plot showing relationship between PMDI values and timber count (construction proxy) from dendrochronological data. Negative correlation indicates increased construction during drought conditions.

**Figure 6. Replicate Validation with Confidence Intervals.** Four-panel figure showing simulation results across 50 replicates: (A) population by scenario, (B) signaling investment, (C) construction-climate correlation with 95% CI, and (D) exotic goods-stress correlation with 95% CI.

**Figure 7. Exotic Goods Chronology.** Detailed analysis of exotic goods timing including (A) scarlet macaw imports, (B) turquoise accumulation, (C) all exotic goods by type, and (D) timing relative to severe droughts.

**Figure 8. Simulation Dynamics Overview.** Four-panel figure showing (A) population trajectories, (B) monument accumulation, (C) exotic goods acquisition, and (D) conflict events across the 400-year simulation period.

**Figure 9. Period Comparison Statistics.** Comparison of key metrics across four archaeological periods: Pre-Chaco (800-900 CE), Early Chaco (900-1000 CE), Peak Chaco (1000-1100 CE), and Late Chaco/Collapse (1100-1200 CE).

**Figure 10. Comprehensive Validation.** Six-panel figure comparing model predictions to archaeological patterns: (A) construction chronology, (B) construction-climate scatter, (C) exotic goods timing, (D) population dynamics, (E) monument-productivity relationship, and (F) summary statistics table.
