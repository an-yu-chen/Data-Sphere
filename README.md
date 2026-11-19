
# Gender Diversity and Scientific Knowledge Sourcing in Green Innovation

## Research overview

Innovation relies on diverse knowledge, inclusive collaboration and the exchange of ideas across individuals and disciplines (Bercovitz & Feldman, 2011; van Rijnsoever et al., 2015; Wagner et al., 2019). This study draws on a dataset of **466,310 green patents granted between 1976 and 2020**, linked to information on scientific publications cited by patents. It finds that patent teams with greater male representation are significantly more likely to cite scientific publications authored by men, whereas the presence of female inventors is associated with increased citations to publications authored by women. Nevertheless, the underrepresentation of female inventors in the green industrial sector examined points to persistent gender inequalities in technological innovation. These findings highlight the importance of gender diversity in shaping knowledge exchange and technological development.

## A. Green innovation over time

The interactive time-series visualisations examine the evolution of green patenting between 1976 and 2020, focusing on annual changes in the number of green patents, the share of patents involving at least one female inventor, trends in the use of scientific knowledge, and changes in inventor team size and selected patent characteristics.

The descriptive findings show that the share of green patents with at least one female inventor increased from approximately **3.6% in 1976 to 24.2% in 2020**. Over the same period, the share of green patents citing scientific publications increased from approximately **13.0% to 35.4%**. These trends provide an overview of the evolution of gender representation and scientific knowledge use in green technological innovation.

## B. Gender representation in green invention

The interactive visualisations further explore gender representation in green invention by comparing female, male and unknown-gender inventor participation. They examine the proportion of female inventors within patent teams, the share of patents involving at least one female inventor, changes in inventor team composition over time, and differences in gender representation across technological fields.

These comparisons provide insights into the evolution of women's participation in green technological innovation and highlight variations in gender representation across technological domains. Importantly, the visualisations present descriptive patterns rather than causal relationships, offering an empirical overview of gender representation in green patenting over time.

## C. Econometric analysis

To complement the descriptive analysis, the project incorporates an econometric investigation of the relationship between inventor gender composition and the gender characteristics of the scientific knowledge cited by green patents. A two-stage Probit specification is employed to examine potential sample selection associated with the availability of scientific-publication gender information and the subsequent likelihood of patents drawing on female-authored scientific knowledge.

### First-stage selection equation

The first stage estimates the probability that a patent has identifiable scientific-publication gender information:

$$
P(S_i=1\mid X_i)=\Phi(X_i'\beta)
$$

Here, $S_i$ denotes the availability of known scientific-publication gender information, while $\Phi$ represents the standard normal cumulative distribution function. The explanatory-variable vector $X_i$ incorporates male inventor share, patent grant year, inventor team size, patent originality, CPC classification count and technological-field indicators.

The first-stage estimation covers **400,219 observations**, with a pseudo-$R^2$ of **0.1861**.

### Second-stage outcome equation

Conditional on selection into the sample, the second-stage model examines the probability that a patent draws on female-authored scientific knowledge:

$$
P(F_i=1\mid Z_i,S_i=1)=\Phi\left(Z_i'\gamma+\delta\widehat{\lambda}_i\right)
$$

Here, $F_i$ denotes whether the patent has a positive female scientific knowledge share, $Z_i$ represents the explanatory variables, and $\widehat{\lambda}_i$ is the inverse Mills ratio estimated from the selection equation.

The second-stage estimation comprises **83,352 observations** and produces a pseudo-$R^2$ of **0.1805**.

The estimates reveal a negative and statistically significant association between the inverse Mills ratio and the female-science indicator (coefficient = **−2.1905**, $p < 0.001$). Male inventor share is likewise negatively associated with the outcome (coefficient = **−0.2919**, $p < 0.001$), while patent grant year exhibits a positive and statistically significant association (coefficient = **0.0326**, $p < 0.001$). The coefficients for inventor team size, patent originality and CPC classification count are not statistically significant at conventional levels.

The interactive presentation enables users to explore coefficient estimates, confidence intervals, marginal effects, sample sizes and model specifications. This facilitates examination of the estimated relationships and provides greater transparency regarding the empirical specification and its results.

### Econometric interpretation and methodological considerations

The findings should be interpreted as conditional associations rather than causal effects. The estimates are presented as results from the specified two-stage procedure. However, interpreting this procedure as a formally corrected sample-selection model requires further econometric validation, particularly concerning the identification strategy, exclusion restrictions and inference procedure.

In particular, conventional second-stage Probit standard errors do not automatically account for the uncertainty associated with the generated inverse Mills ratio. Accordingly, the interactive presentation identifies these estimates as results from the two-stage specification and avoids overstating their inferential or causal implications.

## References

Bercovitz, J., & Feldman, M. (2011). The mechanisms of collaboration in inventive teams: Composition, social networks, and geography. *Research Policy, 40*(1), 81–93.

Chen, A. Y. (2026). *The contribution of scientific knowledge to green technology development: Three essays.* Doctoral dissertation, The University of Manchester. [University of Manchester Research Explorer](https://research.manchester.ac.uk/en/studentTheses/the-contribution-of-scientific-knowledge-to-green-technology-deve/).

Hall, B. H., Jaffe, A. B., & Trajtenberg, M. (2001). *The NBER patent citation data file: Lessons, insights and methodological tools* (NBER Working Paper No. 8498). National Bureau of Economic Research.

Heckman, J. J. (1979). Sample selection bias as a specification error. *Econometrica, 47*(1), 153–161. https://doi.org/10.2307/1912352

Lax-Martinez, G., Raffo, J. D., & Saito, K. (2016). Identifying the gender of PCT inventors. *World Intellectual Property Organization (WIPO) Economic Research Working Paper Series*, (33).

Lin, Z., Yin, Y., Liu, L., & Wang, D. (2023). SciSciNet: A large-scale open data lake for the science of science research. *Scientific Data, 10*(1), 315.

Martinez, G. L., Raffo, J., & Saito, K. (2016). *Identifying the gender of PCT inventors* (Vol. 33). WIPO.

Marx, M., & Fuegi, A. (2020). Reliance on science: Worldwide front-page patent citations to scientific articles. *Strategic Management Journal, 41*(9), 1572–1594.

Marx, M., & Fuegi, A. (2022). Reliance on science by inventors: Hybrid extraction of in-text patent-to-article citations. *Journal of Economics & Management Strategy, 31*(2), 369–392.

Meng, Y. (2016). Collaboration patterns and patenting: Exploring gender distinctions. *Research Policy, 45*(1), 56–67.

Squicciarini, M., Dernis, H., & Criscuolo, C. (2013). *Measuring patent quality: Indicators of technological and economic value* (OECD Science, Technology and Industry Working Papers, No. 2013/03). OECD Publishing.

Trajtenberg, M., Henderson, R., & Jaffe, A. (1997). University versus corporate patents: A window on the basicness of invention. *Economics of Innovation and New Technology, 5*(1), 19–50.

United States Patent and Trademark Office. (n.d.). *PatentsView*. https://data.uspto.gov/support/transition-guide/patentsview

van Buskirk, I., Clauset, A., & Larremore, D. B. (2023, June). An open-source cultural consensus approach to name-based gender classification. In *Proceedings of the International AAAI Conference on Web and Social Media* (Vol. 17, pp. 866–877).

van Rijnsoever, F. J., van den Berg, J., Koch, J., & Hekkert, M. P. (2015). Smart innovation policy: How network position and project composition affect the diversity of an emerging technology. *Research Policy, 44*(5), 1094–1107.

Wagner, C. S., Whetsell, T. A., & Mukherjee, S. (2019). International research collaboration: Novelty, conventionality, and atypicality in knowledge recombination. *Research Policy, 48*(5), 1260–1270.
