import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.patches as mpatches
import numpy as np

df = pd.read_csv("intervalDataRemoveOther.csv")
N = len(df)

# ── Column references ───────────────────────────────────────────────────────
FAC_COL  = "What is your Faculty?"
YR_COL   = "Year of Study?"
DAYS_COL = "On average how many days a week do you use the Open Area?"
STAY_COL = "How long do you plan to be in the Open Area today?"

# ── Ordered categories ──────────────────────────────────────────────────────
FAC_ORDER  = ["UCSC", "FOS", "Arts", "Other"]
YR_ORDER   = ["1st Year", "2nd Year", "3rd Year"]
DAYS_ORDER = ["1 - 2 days", "3 - 4 days", "5+ days"]
STAY_ORDER = ["Less than 30 mins", "30 - 60 mins", "1 - 2 hours", "2+ hours"]

for col, order in [(FAC_COL, FAC_ORDER), (YR_COL, YR_ORDER),
                   (DAYS_COL, DAYS_ORDER), (STAY_COL, STAY_ORDER)]:
    df[col] = pd.Categorical(df[col], categories=order, ordered=True)

# ── Value counts (ordered) ──────────────────────────────────────────────────
fac_vc  = df[FAC_COL].value_counts().reindex(FAC_ORDER,  fill_value=0)
yr_vc   = df[YR_COL].value_counts().reindex(YR_ORDER,   fill_value=0)
days_vc = df[DAYS_COL].value_counts().reindex(DAYS_ORDER, fill_value=0)
stay_vc = df[STAY_COL].value_counts().reindex(STAY_ORDER, fill_value=0)

# ── Colours ─────────────────────────────────────────────────────────────────
FAC_COLORS  = ["#2C7BB6", "#1A9641", "#D7191C", "#8856A7"]
YR_COLORS   = ["#FDAE61", "#F46D43", "#D73027"]
DAYS_COLORS = ["#C6DBEF", "#6BAED6", "#084594"]
STAY_COLORS = ["#EDF8B1", "#7FCDBB", "#2C7FB8", "#253494"]

# ── Helper: annotated horizontal bar ────────────────────────────────────────
def hbar(ax, vc, colors, title, xlabel="Respondents (n)"):
    y   = np.arange(len(vc))
    bars = ax.barh(y, vc.values, color=colors,
                   edgecolor="white", linewidth=0.7, height=0.55)
    ax.set_yticks(y)
    ax.set_yticklabels(vc.index, fontsize=10)
    ax.invert_yaxis()
    for bar, val in zip(bars, vc.values):
        pct = val / N * 100
        ax.text(val + 0.4, bar.get_y() + bar.get_height() / 2,
                f"{val}  ({pct:.1f}%)", va="center", fontsize=9, color="#222")
    ax.set_xlabel(xlabel, fontsize=9)
    ax.set_title(title, fontweight="bold", fontsize=11, pad=7)
    ax.set_xlim(0, vc.max() * 1.38)
    ax.grid(axis="x", linestyle="--", alpha=0.35)
    ax.set_axisbelow(True)
    ax.spines[["top", "right"]].set_visible(False)

# ── Figure ───────────────────────────────────────────────────────────────────
fig = plt.figure(figsize=(16, 12))
gs  = gridspec.GridSpec(2, 2, figure=fig, hspace=0.52, wspace=0.40)

ax1 = fig.add_subplot(gs[0, 0])
ax2 = fig.add_subplot(gs[0, 1])
ax3 = fig.add_subplot(gs[1, 0])
ax4 = fig.add_subplot(gs[1, 1])

hbar(ax1, fac_vc,  FAC_COLORS,  "(a)  Faculty Distribution")
hbar(ax2, yr_vc,   YR_COLORS,   "(b)  Year of Study Distribution")
hbar(ax3, days_vc, DAYS_COLORS, "(c)  Weekly Frequency of Open Area Use")
hbar(ax4, stay_vc, STAY_COLORS, "(d)  Planned Stay Duration Today")

# ── Descriptive summary text boxes ──────────────────────────────────────────
def summary_box(ax, vc, mode_label="Mode"):
    mode_val  = vc.idxmax()
    mode_n    = vc.max()
    mode_pct  = mode_n / N * 100
    txt = (f"{mode_label}: {mode_val}\n"
           f"n = {mode_n}  ({mode_pct:.1f}%)\n"
           f"Total responses: {N}")
    ax.text(0.98, 0.04, txt, transform=ax.transAxes,
            ha="right", va="bottom", fontsize=8.2,
            bbox=dict(boxstyle="round,pad=0.4", facecolor="#F0F0F0",
                      edgecolor="#CCCCCC", alpha=0.9))

summary_box(ax1, fac_vc,  "Dominant faculty")
summary_box(ax2, yr_vc,   "Dominant year")
summary_box(ax3, days_vc, "Most common frequency")
summary_box(ax4, stay_vc, "Most common duration")

fig.suptitle(
    "Descriptive Analysis — Respondent Profile\n"
    "Faculty · Year of Study · Usage Frequency · Stay Duration",
    fontsize=13, fontweight="bold", y=1.01
)

plt.savefig("descriptive_profile.png", dpi=150, bbox_inches="tight")
plt.show()

# ── Console summary ──────────────────────────────────────────────────────────
print(f"Total respondents: {N}\n")
for label, vc in [("Faculty", fac_vc), ("Year of Study", yr_vc),
                  ("Days/Week", days_vc), ("Stay Duration", stay_vc)]:
    print(f"── {label} ──")
    for cat, cnt in vc.items():
        print(f"  {cat:<30} {cnt:>4}  ({cnt/N*100:5.1f}%)")
    print()

print("Saved → descriptive_profile.png")
