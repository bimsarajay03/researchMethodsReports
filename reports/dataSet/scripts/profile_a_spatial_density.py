import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns

df = pd.read_csv("intervalDataRemoveOther.csv")

FACULTY_COL = "What is your Faculty?"
YEAR_COL    = "Year of Study?"
DAYS_COL    = "On average how many days a week do you use the Open Area?"
STAY_COL    = "How long do you plan to be in the Open Area today?"

FACULTY_ORDER = ["UCSC", "FOS", "Arts", "Other"]
YEAR_ORDER    = ["1st Year", "2nd Year", "3rd Year"]
DAYS_ORDER    = ["1 - 2 days", "3 - 4 days", "5+ days"]
STAY_ORDER    = ["Less than 30 mins", "30 - 60 mins", "1 - 2 hours", "2+ hours"]

# Enforce ordering via Categorical
for col, order in [(FACULTY_COL, FACULTY_ORDER), (YEAR_COL, YEAR_ORDER),
                   (DAYS_COL, DAYS_ORDER), (STAY_COL, STAY_ORDER)]:
    df[col] = pd.Categorical(df[col], categories=order, ordered=True)

# ── Helper: build row-normalised % crosstab ────────────────────────────────
def pct_ct(row_var, col_var, row_order, col_order):
    ct = pd.crosstab(df[row_var], df[col_var]).reindex(
        index=row_order, columns=col_order, fill_value=0)
    return ct.div(ct.sum(axis=1), axis=0).mul(100)

# ── Figure: 2 × 2 heatmap grid ────────────────────────────────────────────
fig = plt.figure(figsize=(16, 11))
gs  = gridspec.GridSpec(2, 2, figure=fig, hspace=0.52, wspace=0.40)

HM_KW    = dict(linewidths=0.5, linecolor="white", square=False)
ANNOT_KW = dict(annot_kws={"size": 10, "weight": "bold"})

# (a) Faculty × Year of Study  — raw counts: who are the users?
ax1 = fig.add_subplot(gs[0, 0])
ct_a = pd.crosstab(df[FACULTY_COL], df[YEAR_COL]).reindex(
    index=FACULTY_ORDER, columns=YEAR_ORDER, fill_value=0)
# vmin=-5 shifts the colour scale so even a count of 1 gets a visible shade
sns.heatmap(ct_a, ax=ax1, annot=True, fmt="d", cmap="Blues",
            vmin=-5, cbar_kws={"label": "Respondents (n)"}, **HM_KW, **ANNOT_KW)
ax1.set_title("(a) User Profile: Faculty × Year of Study\n(raw counts)", fontweight="bold", fontsize=11)
ax1.set_xlabel("Year of Study", fontsize=10)
ax1.set_ylabel("Faculty", fontsize=10)
ax1.tick_params(axis="x", rotation=0)
ax1.tick_params(axis="y", rotation=0)

# (b) Year of Study × Days per Week  — % within year: usage frequency
ax2 = fig.add_subplot(gs[0, 1])
pct_b = pct_ct(YEAR_COL, DAYS_COL, YEAR_ORDER, DAYS_ORDER)
sns.heatmap(pct_b, ax=ax2, annot=True, fmt=".1f", cmap="YlOrRd",
            vmin=0, vmax=100, cbar_kws={"label": "% within Year"}, **HM_KW, **ANNOT_KW)
ax2.set_title("(b) Usage Frequency: Year of Study × Days/Week\n(row %)", fontweight="bold", fontsize=11)
ax2.set_xlabel("Days per Week", fontsize=10)
ax2.set_ylabel("Year of Study", fontsize=10)
ax2.tick_params(axis="x", rotation=0)
ax2.tick_params(axis="y", rotation=0)

# (c) Faculty × Stay Duration  — % within faculty
ax3 = fig.add_subplot(gs[1, 0])
pct_c = pct_ct(FACULTY_COL, STAY_COL, FACULTY_ORDER, STAY_ORDER)
sns.heatmap(pct_c, ax=ax3, annot=True, fmt=".1f", cmap="YlGn",
            vmin=0, vmax=100, cbar_kws={"label": "% within Faculty"}, **HM_KW, **ANNOT_KW)
ax3.set_title("(c) Stay Duration by Faculty\n(row %)", fontweight="bold", fontsize=11)
ax3.set_xlabel("Planned Stay Duration", fontsize=10)
ax3.set_ylabel("Faculty", fontsize=10)
ax3.set_xticklabels(ax3.get_xticklabels(), rotation=25, ha="right", fontsize=9)
ax3.tick_params(axis="y", rotation=0)

# (d) Year of Study × Stay Duration  — % within year
ax4 = fig.add_subplot(gs[1, 1])
pct_d = pct_ct(YEAR_COL, STAY_COL, YEAR_ORDER, STAY_ORDER)
sns.heatmap(pct_d, ax=ax4, annot=True, fmt=".1f", cmap="PuBu",
            vmin=0, vmax=100, cbar_kws={"label": "% within Year"}, **HM_KW, **ANNOT_KW)
ax4.set_title("(d) Stay Duration by Year of Study\n(row %)", fontweight="bold", fontsize=11)
ax4.set_xlabel("Planned Stay Duration", fontsize=10)
ax4.set_ylabel("Year of Study", fontsize=10)
ax4.set_xticklabels(ax4.get_xticklabels(), rotation=25, ha="right", fontsize=9)
ax4.tick_params(axis="y", rotation=0)

fig.suptitle(
    "Demographic & Baseline Spatial-Temporal Profiles\n"
    "Profile A: Spatial Density and Stay-Duration Matrix",
    fontsize=13, fontweight="bold", y=1.02
)

plt.savefig("profile_a_spatial_density.png", dpi=150, bbox_inches="tight")
plt.show()

print("Chart saved as profile_a_spatial_density.png")
print("\n── (a) Raw counts ──\n", ct_a.to_string())
print("\n── (b) Days/Week % ──\n", pct_b.round(1).to_string())
print("\n── (c) Stay Duration by Faculty % ──\n", pct_c.round(1).to_string())
print("\n── (d) Stay Duration by Year % ──\n", pct_d.round(1).to_string())
