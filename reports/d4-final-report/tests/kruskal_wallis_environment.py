"""
Kruskal-Wallis H-test: Environmental comfort ratings across the four diurnal intervals.
Dataset: intervalDataRemoveOther.csv (N = 133)

H0: The distribution of environmental comfort ratings is identical across all
    four diurnal time blocks.
H1: At least one diurnal time block has a significantly different distribution
    of environmental comfort ratings compared to the others.
"""
import pandas as pd
from scipy.stats import kruskal

DATA_PATH = "intervalDataRemoveOther.csv"
INTERVAL_ORDER = ["Morning", "Midday", "Afternoon", "Evening"]
VARIABLES = ["Thermal Comfort", "Occupancy Level"]

df = pd.read_csv(DATA_PATH)

rows = []
for var in VARIABLES:
    groups = [df.loc[df["Interval"] == interval, var] for interval in INTERVAL_ORDER]
    h_stat, p_value = kruskal(*groups)
    rows.append({
        "Variable": var,
        "H-statistic": round(h_stat, 3),
        "df": len(INTERVAL_ORDER) - 1,
        "p-value": "<0.001" if p_value < 0.001 else round(p_value, 4),
        "Significant (a=0.05)": "Yes" if p_value < 0.05 else "No",
    })

results = pd.DataFrame(rows)
results.to_csv("kruskal_wallis_results.csv", index=False)

medians = df.groupby("Interval")[VARIABLES].median().reindex(INTERVAL_ORDER)
medians.to_csv("kruskal_wallis_medians.csv")

print(results.to_string(index=False))
print("\nMedian ratings by interval:")
print(medians)
