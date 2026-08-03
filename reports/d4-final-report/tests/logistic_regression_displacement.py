"""
Binary Logistic Regression: predicting student displacement under a sudden
noise disruption from environmental stressor ratings.
Dataset: intervalDataRemoveOther.csv (N = 133)

Outcome (binary): would the student leave the Open Area entirely if it
became significantly louder due to a social event?
    0 = Stay (tolerate the noise, or switch to casual socialising)
    1 = Leave (relocate to another building)

Predictors: Thermal Comfort, Noise Level, Occupancy Level (all rated 1-5,
current conditions, ordinal treated as continuous scores per common practice).

H0: Thermal Comfort, Noise Level, and Occupancy Level do not predict the
    probability of a student leaving the Open Area under a noise disruption
    (all coefficients = 0).
H1: At least one of Thermal Comfort, Noise Level, or Occupancy Level
    significantly predicts the probability of leaving.
"""
import pandas as pd
import statsmodels.api as sm

DATA_PATH = "intervalDataRemoveOther.csv"
NOISE_REACTION_COL = "If this space became significantly louder right now due to a social event what would you do?"

df = pd.read_csv(DATA_PATH)

df["WouldLeave"] = df[NOISE_REACTION_COL].str.startswith("Leave").astype(int)

predictors = ["Thermal Comfort", "Noise Level", "Occupancy Level"]
X = sm.add_constant(df[predictors])
y = df["WouldLeave"]

model = sm.Logit(y, X).fit(disp=0)

summary_df = pd.DataFrame({
    "Predictor": ["Intercept"] + predictors,
    "Coefficient": model.params.round(3).values,
    "Std. Error": model.bse.round(3).values,
    "p-value": model.pvalues.round(4).values,
    "Odds Ratio": pd.Series(model.params).apply(lambda b: round(2.71828 ** b, 3)).values,
})
summary_df.to_csv("logistic_regression_results.csv", index=False)

fit_stats = pd.DataFrame([{
    "N": int(model.nobs),
    "Pseudo R-sq (McFadden)": round(model.prsquared, 3),
    "LLR p-value": round(model.llr_pvalue, 4),
}])
fit_stats.to_csv("logistic_regression_fit.csv", index=False)

print(model.summary())
print("\nOutcome distribution:")
print(df["WouldLeave"].value_counts())
print("\n", summary_df)
print("\n", fit_stats)
