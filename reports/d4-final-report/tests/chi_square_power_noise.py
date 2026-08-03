"""
Chi-Square Test of Independence: Power Dependency x reaction to a sudden
noise disruption (stay vs leave).
Dataset: intervalDataRemoveOther.csv (N = 133)

H0: Reaction to a noise disruption (stay vs leave) is independent of
    power dependency.
H1: Reaction to a noise disruption is associated with power dependency.
"""
import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency

DATA_PATH = "intervalDataRemoveOther.csv"
POWER_COL = "Are you currently using an electronic device (laptop/phone/tablet) that requires a continuous power supply to stay here?"
NOISE_REACTION_COL = "If this space became significantly louder right now due to a social event what would you do?"

df = pd.read_csv(DATA_PATH)

df["Reaction"] = np.where(df[NOISE_REACTION_COL].str.startswith("Leave"), "Leave", "Stay")

power_order = ["No", "Yes, but I am running on battery power", "Yes, and I am currently plugged into a wall socket"]
contingency = pd.crosstab(df[POWER_COL], df["Reaction"]).reindex(power_order)
contingency.to_csv("chi_square_power_noise_contingency.csv")

chi2, p, dof, expected = chi2_contingency(contingency)
n = contingency.to_numpy().sum()
min_dim = min(contingency.shape) - 1
cramers_v = np.sqrt((chi2 / n) / min_dim)

results = pd.DataFrame([{
    "N": n,
    "Chi-square": round(chi2, 3),
    "df": dof,
    "p-value": "<0.001" if p < 0.001 else round(p, 4),
    "Cramers_V": round(cramers_v, 3),
}])
results.to_csv("chi_square_power_noise_results.csv", index=False)

print("Contingency table (observed counts):")
print(contingency)
print("\nRow percentages (leave rate by power dependency):")
print((contingency.div(contingency.sum(axis=1), axis=0) * 100).round(1))
print("\nChi-square:", round(chi2, 3), "df:", dof, "p-value:", p)
print("Cramer's V:", round(cramers_v, 3))
