"""
Chi-Square Test of Independence: Time Interval x Activity Type (Academic vs Non-academic)
Dataset: intervalDataRemoveOther.csv (N = 133)

H0: Activity type (Academic / Non-academic) is independent of time interval.
H1: Activity type is associated with time interval.
"""
import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency

DATA_PATH = "intervalDataRemoveOther.csv"
ACTIVITY_COL = "What activities are you doing in the Open Area today?"

df = pd.read_csv(DATA_PATH)

# Collapse the activity column to a binary Academic / Non-academic split.
# A response is classed as "Academic" if it reports any academic work
# (individual or collaborative), even when combined with a secondary
# non-academic activity; otherwise it is classed as "Non-academic".
df["ActivityGroup"] = np.where(
    df[ACTIVITY_COL].str.contains("Academic Work", case=False, na=False),
    "Academic",
    "Non-academic",
)

interval_order = ["Morning", "Midday", "Afternoon", "Evening"]
contingency = pd.crosstab(df["Interval"], df["ActivityGroup"]).reindex(interval_order)
contingency.to_csv("contingency_table.csv")

chi2, p, dof, expected = chi2_contingency(contingency)

n = contingency.to_numpy().sum()
min_dim = min(contingency.shape) - 1
cramers_v = np.sqrt((chi2 / n) / min_dim)

results = pd.DataFrame(
    [{
        "N": n,
        "Chi-square": round(chi2, 3),
        "df": dof,
        "p-value": round(p, 4),
        "Cramers_V": round(cramers_v, 3),
    }]
)
results.to_csv("chi_square_results.csv", index=False)

print("Contingency table (observed counts):")
print(contingency)
print("\nExpected counts:")
print(pd.DataFrame(expected, index=contingency.index, columns=contingency.columns).round(2))
print("\nChi-square:", round(chi2, 3), "df:", dof, "p-value:", round(p, 4))
print("Cramer's V:", round(cramers_v, 3))
