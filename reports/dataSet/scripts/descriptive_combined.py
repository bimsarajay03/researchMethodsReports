import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import seaborn as sns

df = pd.read_csv("intervalDataRemoveOther.csv")
N = len(df)

FAC_COL  = "What is your Faculty?"
YR_COL   = "Year of Study?"
DAYS_COL = "On average how many days a week do you use the Open Area?"
STAY_COL = "How long do you plan to be in the Open Area today?"

FAC_ORDER  = ["UCSC", "FOS", "Arts", "Other"]
YR_ORDER   = ["1st Year", "2nd Year", "3rd Year"]
DAYS_ORDER = ["1 - 2 days", "3 - 4 days", "5+ days"]
STAY_ORDER = ["Less than 30 mins", "30 - 60 mins", "1 - 2 hours", "2+ hours"]

for col, order in [(FAC_COL, FAC_ORDER), (YR_COL, YR_ORDER),
                   (DAYS_COL, DAYS_ORDER), (STAY_COL, STAY_ORDER)]:
    df[col] = pd.Categorical(df[col], categories=order, ordered=True)

# ── Colour palettes ─────────────────────────────────────────────────────────
YR_COLORS   = {"1st Year": "#FDAE61", "2nd Year": "#E6550D", "3rd Year": "#A63603"}
DAYS_COLORS = {"1 - 2 days": "#C6DBEF", "3 - 4 days": "#4292C6", "5+ days": "#084594"}
STAY_COLORS = {
    "Less than 30 mins": "#EDF8B1",
    "30 - 60 mins":      "#7FCDBB",
    "1 - 2 hours":       "#1D91C0",
    "2+ hours":          "#0C2C84",
}
FAC_COLORS  = {"UCSC": "#2C7BB6", "FOS": "#1A9641", "Arts": "#D7191C", "Other": "#8856A7"}

# ── Helper: 100% stacked horizontal bar ─────────────────────────────────────
def stacked_100_hbar(ax, row_col, col_col, row_order, col_order,
                     col_colors, title, raw_counts=None):
    ct  = pd.crosstab(df[row_col], df[col_col]).reindex(
              index=row_order, columns=col_order, fill_value=0)
    pct = ct.div(ct.sum(axis=1), axis=0) * 100

    y    = np.arange(len(row_order))
    left = np.zeros(len(row_order))

    for col_cat in col_order:
        vals = pct[col_cat].values
        ax.barh(y, vals, left=left,
                color=col_colors[col_cat], edgecolor="white",
                linewidth=0.6, label=col_cat, height=0.60)
        for i, (v, l) in enumerate(zip(vals, left)):
            if v >= 9:
                ax.text(l + v / 2, i, f"{v:.0f}%",
                        ha="center", va="center",
                        fontsize=8.5, color="white", fontweight="bold")
        left += vals

    # Row totals on the right
    totals = ct.sum(axis=1)
    for i, (row_label, tot) in enumerate(zip(row_order, totals)):
        ax.text(101, i, f"n={tot}", va="center", fontsize=8, color="#555")

    ax.set_yticks(y)
    ax.set_yticklabels(row_order, fontsize=10)
    ax.set_xlim(0, 113)
    ax.set_xlabel("% within group", fontsize=9)
    ax.set_title(title, fontweight="bold", fontsize=11, pad=6)
    ax.axvline(50, color="grey", linewidth=0.5, linestyle=":", alpha=0.6)
    ax.grid(axis="x", linestyle="--", alpha=0.28)
    ax.set_axisbelow(True)
    ax.spines[["top", "right"]].set_visible(False)
    ax.invert_yaxis()
    ax.legend(loc="lower right", fontsize=8, framealpha=0.85,
              title_fontsize=8, borderpad=0.4)

# ── Figure ───────────────────────────────────────────────────────────────────
fig = plt.figure(figsize=(18, 15))
gs  = gridspec.GridSpec(2, 2, figure=fig, hspace=0.52, wspace=0.42)

ax1 = fig.add_subplot(gs[0, 0])
ax2 = fig.add_subplot(gs[0, 1])
ax3 = fig.add_subplot(gs[1, 0])
ax4 = fig.add_subplot(gs[1, 1])

# (a) For each Faculty → what Year mix?
stacked_100_hbar(ax1, FAC_COL, YR_COL, FAC_ORDER, YR_ORDER, YR_COLORS,
                 "(a)  Year of Study Composition by Faculty")

# (b) For each Faculty → how often do they come?
stacked_100_hbar(ax2, FAC_COL, DAYS_COL, FAC_ORDER, DAYS_ORDER, DAYS_COLORS,
                 "(b)  Weekly Usage Frequency by Faculty")

# (c) For each Faculty → how long do they stay?
stacked_100_hbar(ax3, FAC_COL, STAY_COL, FAC_ORDER, STAY_ORDER, STAY_COLORS,
                 "(c)  Stay Duration by Faculty")

# (d) Do heavier users stay longer?
#     Days/Week × Stay Duration — row-normalised % heatmap
ct_d = pd.crosstab(df[DAYS_COL], df[STAY_COL]).reindex(
           index=DAYS_ORDER, columns=STAY_ORDER, fill_value=0)
pct_d = ct_d.div(ct_d.sum(axis=1), axis=0) * 100

# Custom annotation: "n\n(pct%)"
annot = ct_d.astype(str) + "\n(" + pct_d.round(0).astype(int).astype(str) + "%)"

sns.heatmap(pct_d, ax=ax4,
            annot=annot, fmt="", cmap="YlOrRd",
            vmin=0, vmax=60,
            linewidths=0.6, linecolor="white",
            cbar_kws={"label": "% within frequency group"},
            annot_kws={"size": 9, "weight": "bold"})

ax4.set_title("(d)  Do More Frequent Visitors Stay Longer?\n"
              "Days/Week × Stay Duration  (n and row %)",
              fontweight="bold", fontsize=11, pad=6)
ax4.set_xlabel("Planned Stay Duration", fontsize=10)
ax4.set_ylabel("Days per Week", fontsize=10)
ax4.tick_params(axis="x", rotation=20, labelsize=9)
ax4.tick_params(axis="y", rotation=0,  labelsize=10)
ax4.set_xticklabels(ax4.get_xticklabels(), ha="right")

fig.suptitle(
    "Combined Descriptive Profile — Open Area Respondents  (n = 133)\n"
    "Relationships between Faculty · Year of Study · Usage Frequency · Stay Duration",
    fontsize=13, fontweight="bold", y=1.01
)

plt.savefig("descriptive_combined.png", dpi=150, bbox_inches="tight")
plt.show()

# ── Console cross-tabs ───────────────────────────────────────────────────────
for row, col, ro, co, lbl in [
    (FAC_COL, YR_COL,   FAC_ORDER, YR_ORDER,   "Faculty × Year"),
    (FAC_COL, DAYS_COL, FAC_ORDER, DAYS_ORDER, "Faculty × Days/Week"),
    (FAC_COL, STAY_COL, FAC_ORDER, STAY_ORDER, "Faculty × Stay Duration"),
    (DAYS_COL, STAY_COL, DAYS_ORDER, STAY_ORDER, "Days/Week × Stay Duration"),
]:
    ct = pd.crosstab(df[row], df[col]).reindex(index=ro, columns=co, fill_value=0)
    print(f"\n── {lbl} (counts) ──\n{ct.to_string()}")

print("\nSaved → descriptive_combined.png")
