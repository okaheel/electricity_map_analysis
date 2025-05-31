## “A short look-back Spatio‐Temporal Analysis and near term forecast of Carbon Intensity in U.S. Electricity Generation”

As there is a reindustrialization wave happening across the United States, this has large implications of 

This project will quantify, map, and forecast the hourly carbon intensity (CO₂ per MWh) of electricity generation across U.S. Balancing Authorities (BAs). We will combine:

EIA Electric Grid Monitor (Hourly Operations) (EIA‐930 API)—hourly, BA‐level generation by fuel type and demand (2018–present).

EPA eGRID (Emissions & Generation Resource Integrated Database)—plant‐level annual generation and emissions (CO₂, NOₓ, SO₂, etc.) with geolocation (lat/lon), fuel type, and (where available) BA or state.

By linking plants to BAs (via spatial joins) and computing BA‐ and fuel‐specific emission rates (tons CO₂/MWh), we will estimate hourly CO₂ emissions for each BA (combining that rate with EIA’s hourly generation by fuel). The analysis has two main thrusts:

1. Time‐Series Analysis: Decompose BA‐level hourly CO₂ intensity into trend + seasonal components; build and validate short‐term forecasting models (e.g., SARIMA, Gradient Boosting or LSTM) for next‐day BA emissions

2. Geospatial Analysis: Create static and interactive maps showing spatial “hotspots” of high emission intensity—both at the BA level and at individual power plants—identify clustering patterns (e.g., BAs that remain carbon‐heavy vs. those that are cleaner)

3. If at all possible (time and data permitting), I would like to see if there is any way to pull a data center data set and use that to present a average estimate of load consumption vs emissions intensity for data centers
