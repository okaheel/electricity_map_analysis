## “A short look-back Spatio‐Temporal Analysis and near term forecast of Carbon Intensity in U.S. Electricity Generation”


### Background
As there is a reindustrialization wave happening across the United States, this has large implications on energy generation and consumption patterns. Understanding carbon intensity, electricity generation sources and other variables would allow us to develop a better understanding of patterns that emerging along with risk, impacts or trends of interest that are popping up.

There are a lot of methodologies that the industry has developed for quantifying electricity related emissions, and many of them depend on how exactly you define the emissions you are trying to quantify, so this will be relatively rudimentary quantification of average emissions across U.S. Balancing Authorities (BAs). Industry standard is marginal emissions, [here](https://watttime.org/data-science/data-signals/average-vs-marginal/) is a link to a primer on marginal emissions. And as I have spent a significant amount of time helping develop the methodology that my employer [Ascend Analytics](https://www.ascendanalytics.com/blog/unlocking-the-carbon-abatement-potential-of-storage-with-locational-marginal-emissions) uses, I will steer a little clear of that to avoid potential conflicts of interest.

With this in mind, this project will use publicly available data for carbon intensity, demand and such to see if there are patterns that emerge.

---

### Description

This project will quantify, map, and forecast the hourly carbon intensity (CO₂ per MWh) of electricity generation across U.S. BAs. We will combine:

EIA Electric Grid Monitor (Hourly Operations) (EIA‐930 API)—hourly, BA‐level generation by fuel type and demand (2018–present).

EPA eGRID (Emissions & Generation Resource Integrated Database)—plant‐level annual generation and emissions (CO₂, NOₓ, SO₂, etc.) with geolocation (lat/lon), fuel type, and (where available) BA or state.

### Research questions:

1. How has hourly CO₂ intensity (tons CO₂/MWh) evolved at the BA level over the past 3–5 years?

    - What are the dominant seasonal and daily patterns?

2. Which geographic regions (BAs or clusters of plants) consistently exhibit high CO₂ intensity?

    - How do plant‐level factors (fuel mix, age, location) correlate with “hotspot” BAs?

3. Can we accurately forecast next‐day hourly CO₂ emissions for a given BA using historical generation and (optionally) calendar or weather features?

    - What is the predictive performance difference between classical time series models (e.g., SARIMA) versus machine learning approaches (e.g., XGBoost, LSTM)?


---

### Implementation and needed pieces:

To successfully build this project here are the three required pieces:

1. Data Integration & Join Logic

    - There are multiple different data sources that will likely be needed. It will be a mixture of data from EPA, EIA, and other industry sources. This will enable good industry quality analysis

2. Analysis architecture and presentation

    - There will need to be some organization of code as there will be various pieces involved. So this piece will be building out the script and tools that are need for documenting and presenting findings. I will likely put most of this in a streamlit dashboard to showcase the work.

3. Modeling and experimentation

    - As this is a data mining project, a core component is the actual model and results that come from it


---

### Approach

By linking plants to BAs (via spatial joins) and computing BA‐ and fuel‐specific emission rates (tons CO₂/MWh), we will estimate hourly CO₂ emissions for each BA (combining that rate with EIA’s hourly generation by fuel). The analysis has two main thrusts:

1. Time‐Series Analysis: Decompose BA‐level hourly CO₂ intensity into trend + seasonal components; build and validate short‐term forecasting models (e.g., SARIMA, Gradient Boosting or LSTM) for next‐day BA emissions

2. Geospatial Analysis: Create static and interactive maps showing spatial “hotspots” of high emission intensity—both at the BA level and at individual power plants—identify clustering patterns (e.g., BAs that remain carbon‐heavy vs. those that are cleaner)

3. If at all possible (time and data permitting), I would like to see if there is any way to pull a data center data set and use that to present a average estimate of load consumption vs emissions intensity for data centers (existing and upcoming)
