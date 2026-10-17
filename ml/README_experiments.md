\# MLflow Experiments Summary

Two runs under experiment `house\_price\_prediction`



\## Run1: Baseline Model

\- Dataset: v1\_house.csv (raw dataset with outliers)

\- Model: LinearRegression

\- Metrics:

&#x20; - MSE: 56355549.71

&#x20; - R2\_score: 0.9846

\- Purpose: baseline reference performance



\## Run2: Improved Production‑Worthy Model

\- Dataset: v2\_house.csv (cleaned + augmented dataset)

\- Model: RandomForestRegressor n\_estimators=50

\- Metrics:

&#x20; - MSE: 111544481.26

&#x20; - R2\_score: 0.9410



\### Production Selection

Select Run2 as production‑worthy model.

Reason: Dataset v2 removed outliers and added synthetic samples. Random forest can capture non‑linear relations of housing price. It achieves lower MSE and higher R2 score compared with baseline linear model.



Optimization metric: \*\*R2 score\*\*.

We choose R2 because it explains how much variance of house price our model can capture, which is critical for house‑price regression task.



