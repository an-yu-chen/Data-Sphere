
# Gender, Scientific Knowledge and Green Innovation
## Interactive Research Visualisations and Knowledge Network Analysis

An interactive research project exploring gender representation, scientific knowledge sourcing and innovation characteristics across 466,310 green patents from 1976 to 2020.

The project combines descriptive data visualisation, Python-based data processing and network analysis to explore how scientific knowledge connects to technological innovation.

## Research objectives

- Explore the evolution of green patenting over time.
- Examine gender representation among patent inventors.
- Investigate the relationship between scientific publications and green technological innovation.
- Explore knowledge connections between patents and scientific publications.
- Demonstrate reproducible data processing and analytical workflows.

## Project structure

```text
green-innovation-research/
│
├── README.md
├── index.html
├── script.js
└── style.css
```

## Interactive research visualisations

The website is organised around four analytical themes.

### 1. Green innovation trends

Annual patenting activity between 1976 and 2020, including:
- Patent counts
- Changes in inventor team size
- Science-using patent shares

### 2. Gender and innovation

Descriptive exploration of:
- Female inventor representation
- Male inventor representation
- Unknown-gender representation
- Patents with at least one female inventor

### 3. Scientific knowledge sourcing

Exploration of:
- Patents linked to scientific publications
- Female-authored scientific knowledge shares
- Male-authored scientific knowledge shares
- Changes in science–technology connections over time

### 4. Knowledge network analysis

The project can represent patent–publication relationships as a bipartite network.

In this structure:
- Patent nodes represent technological inventions.
- Publication nodes represent scientific knowledge sources.
- Edges represent observed patent–publication relationships.

Potential network indicators include:
- Degree centrality
- Weighted degree
- Network density
- Connected components
- Community structure
- Knowledge-source concentration

These indicators should be calculated from the actual edge list before being interpreted as empirical findings.

An inventor co-invention network could also be developed if inventor-level identifiers and collaboration links are available.

## Data and analytical workflow

The research dataset contains 466,310 patent observations covering 1976–2020.

The annual visualisations use descriptive aggregates prepared from the patent-level dataset.

The network analysis requires a patent–publication edge list derived from the patent–paper linkage data.

### Expected CSV files

The website accepts three CSV files:

**1. `yearly_patent_indicators.csv`**

Expected columns:

```text
YearOfPatentGrant
patent_count
mean_female_ratio
mean_male_ratio
mean_unknown_gender_ratio
patents_with_female_inventors
patents_with_male_inventors
average_team_size
science_using_patents
average_originality
average_generality
average_forward_citations_5yr
average_forward_citations_7yr
female_inventor_patent_share
science_using_patent_share
```

**2. `yearly_science_indicators.csv`**

Expected columns:

```text
YearOfPatentGrant
science_patent_count
mean_female_science_share
mean_male_science_share
```

**3. `patent_paper_edges.csv`**

Expected columns:

```text
source
target
weight
```

Here, `source` is a patent identifier and `target` is a scientific publication identifier. `weight` is optional and should reflect a documented linkage measure.

The website does not contain the original patent-level dataset.

## Python methods and reproducibility

The analytical workflow is designed around Python, Pandas and NetworkX.

### Step 1: Data preparation

```python
import pandas as pd

patents = pd.read_csv(
    "genderpatent_with_gender_ratios.csv",
    dtype={"patent_id": str}
)

print(patents.shape)
print(patents.info())
```

### Step 2: Annual indicators

```python
yearly = (
    patents.groupby("YearOfPatentGrant")
    .agg(
        patent_count=("patent_id", "count"),
        mean_female_ratio=("female_ratio", "mean"),
        mean_male_ratio=("male_ratio", "mean"),
        average_team_size=("team_size", "mean"),
        science_using_patents=("Uses_Science", "sum")
    )
    .reset_index()
)

yearly["female_inventor_patent_share"] = (
    patents.assign(
        has_female=patents["female_ratio"] > 0
    )
    .groupby("YearOfPatentGrant")["has_female"]
    .mean()
    .values
)
```

### Step 3: Constructing a patent–publication network

The patent–paper linkage data can be used to construct a bipartite network.

```python
import pandas as pd
import networkx as nx

links = pd.read_stata("_patent_paper_pairs.dta")

edges = links[["patent", "paperid"]].drop_duplicates()

edges = edges.rename(columns={
    "patent": "source",
    "paperid": "target"
})

edges["weight"] = 1

edges.to_csv(
    "patent_paper_edges.csv",
    index=False
)
```

### Step 4: Network analysis

```python
import networkx as nx
import pandas as pd

edges = pd.read_csv("patent_paper_edges.csv")

G = nx.Graph()

for _, row in edges.iterrows():
    G.add_node(row["source"], bipartite="patent")
    G.add_node(row["target"], bipartite="publication")
    G.add_edge(
        row["source"],
        row["target"],
        weight=row["weight"]
    )

degree = dict(G.degree())
weighted_degree = dict(G.degree(weight="weight"))

network_summary = pd.DataFrame({
    "node": list(G.nodes()),
    "degree": [degree[n] for n in G.nodes()],
    "weighted_degree": [
        weighted_degree[n] for n in G.nodes()
    ]
})
```

This is a starting point. Before calculating network statistics, identifiers must be normalised and patent and publication node namespaces must be kept separate.

A projected patent–patent network can be constructed by connecting patents that cite or share scientific publications. The projection should be documented because it changes the interpretation of network relationships.

## Data architecture

The proposed architecture separates data sources, processing, analytical outputs and visual presentation.

```text
SOURCE DATA
    |
    |-- Patent-level dataset
    |
    |-- Patent–publication linkage data
    |
    v
DATA PREPARATION
    |
    |-- Data validation
    |-- Identifier standardisation
    |-- Missing-value checks
    |-- Variable construction
    |
    v
ANALYTICAL LAYER
    |
    |-- Annual descriptive indicators
    |-- Gender indicators
    |-- Science-sourcing indicators
    |-- Patent–publication network
    |
    v
OUTPUT DATA
    |
    |-- yearly_patent_indicators.csv
    |-- yearly_science_indicators.csv
    |-- patent_paper_edges.csv
    |
    v
INTERACTIVE PRESENTATION
    |
    |-- Trend visualisations
    |-- Gender comparisons
    |-- Science–technology relationships
    |-- Network exploration
```

## Tools and technologies

- Python
- Pandas
- NumPy
- NetworkX
- Plotly.js
- JavaScript
- HTML5 and CSS3
- Git and GitHub

## Methodological note

The annual charts are descriptive and should not be interpreted as causal estimates.

Network indicators depend on the definition of nodes, edges, weights and network boundaries. The patent–publication network represents knowledge relationships, not necessarily direct social interaction between individuals.

The interactive website is a presentation layer. Statistical modelling and network construction should be conducted and documented in Python.

## Research integrity

The project should be shared in accordance with the authors' permissions, data licences and any applicable confidentiality requirements.

No confidential source data should be uploaded to the public repository without explicit authorisation.

## Future development

Potential extensions include:

- Inventor co-invention networks
- Community detection
- Patent–publication network projections
- Temporal network analysis
- Firm-level knowledge networks
- Additional interactive filters and analytical comparisons
