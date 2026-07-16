import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
from matplotlib.patches import Rectangle

df = pd.read_csv("intervalDataRemoveOther.csv")

FACULTY_COL = "What is your Faculty?"
YEAR_COL    = "Year of Study?"
DAYS_COL    = "On average how many days a week do you use the Open Area?"
STAY_COL    = "How long do you plan to be in the Open Area today?"

FACULTY_ORDER = ["UCSC", "FOS", "Arts", "Other"]
YEAR_ORDER    = ["1st Year", "2nd Year", "3rd Year"]
DAYS_ORDER    = ["1 - 2 days", "3 - 4 days", "5+ days"]
STAY_ORDER    = ["Less than 30 mins", "30 - 60 mins", "1 - 2 hours", "2+ hours"]

FAC_COLORS  = {"UCSC": "#4C72B0", "FOS": "#55A868", "Arts": "#C44E52", "Other": "#8172B2"}
YEAR_COLORS = {"1st Year": "#E67E22", "2nd Year": "#2980B9", "3rd Year": "#27AE60"}

# ── Power user definition: 5+ days/week AND 2+ hours planned stay ──────────
df["Power User"] = (df[DAYS_COL] == "5+ days") & (df[STAY_COL] == "2+ hours")

# ── Numeric axes for bubble chart ──────────────────────────────────────────
days_pos = {d: i for i, d in enumerate(DAYS_ORDER)}
stay_pos = {s: i for i, s in enumerate(STAY_ORDER)}

# Faculty horizontal offsets within each cell so bubbles don't overlap
FAC_OFFSET = {"UCSC": -0.18, "FOS": -0.06, "Arts": 0.06, "Other": 0.18}

# ── Layout ─────────────────────────────────────────────────────────────────
fig = plt.figure(figsize=(17, 10))
gs  = gridspec.GridSpec(2, 2, figure=fig,
                        width_ratios=[2, 1], hspace=0.50, wspace=0.38)

# ══════════════════════════════════════════════════════════════════════════
# Panel (a): Bubble density matrix  — Days/Week × Stay Duration
# ══════════════════════════════════════════════════════════════════════════
ax1 = fig.add_subplot(gs[:, 0])

for faculty in FACULTY_ORDER:
    sub = df[df[FACULTY_COL] == faculty]
    plotted_label = False
    for days in DAYS_ORDER:
        for stay in STAY_ORDER:
            cnt = int(((sub[DAYS_COL] == days) & (sub[STAY_COL] == stay)).sum())
            if cnt == 0:
                continue
            x = days_pos[days] + FAC_OFFSET[faculty]
            y = stay_pos[stay]
            ax1.scatter(x, y, s=cnt * 80,
                        color=FAC_COLORS[faculty],
                        alpha=0.80, edgecolors="white", linewidths=0.9,
                        zorder=3, label=faculty if not plotted_label else "")
            plotted_label = True
            ax1.text(x, y, str(cnt), ha="center", va="center",
                     fontsize=8.5, fontweight="bold", color="white", zorder=4)

# Highlight the power-user zone (top-right cell: 5+ days, 2+ hours)
ax1.add_patch(Rectangle((1.4, 2.45), 1.1, 1.1,
                         linewidth=2, edgecolor="#E74C3C",
                         facecolor="#E74C3C", alpha=0.10, zorder=1))
ax1.text(2.95, 3.5, "Power\nUser Zone", ha="right", va="top",
         fontsize=9, color="#C0392B", fontweight="bold", style="italic")

# Grid lines between cells
for i in range(len(DAYS_ORDER) - 1):
    ax1.axvline(i + 0.5, color="grey", linewidth=0.5, linestyle="--", alpha=0.5)
for j in range(len(STAY_ORDER) - 1):
    ax1.axhline(j + 0.5, color="grey", linewidth=0.5, linestyle="--", alpha=0.5)

ax1.set_xticks(range(len(DAYS_ORDER)))
ax1.set_xticklabels(DAYS_ORDER, fontsize=11)
ax1.set_yticks(range(len(STAY_ORDER)))
ax1.set_yticklabels(STAY_ORDER, fontsize=11)
ax1.set_xlim(-0.5, 2.5)
ax1.set_ylim(-0.5, 3.8)
ax1.set_xlabel("Days per Week in Open Area", fontsize=12)
ax1.set_ylabel("Planned Stay Duration", fontsize=12)
ax1.set_title("(a) Spatial Density Bubble Map\nDays/Week × Stay Duration  |  Bubble size ∝ respondent count",
              fontweight="bold", fontsize=12)

# Legend: faculty colours + bubble size guide
handles, labels = ax1.get_legend_handles_labels()
seen = {}
for h, l in zip(handles, labels):
    if l not in seen:
        seen[l] = h
size_handles = [
    plt.scatter([], [], s=1*80,  color="grey", alpha=0.7, label="n = 1"),
    plt.scatter([], [], s=5*80,  color="grey", alpha=0.7, label="n = 5"),
    plt.scatter([], [], s=10*80, color="grey", alpha=0.7, label="n = 10"),
]
leg1 = ax1.legend(list(seen.values()), list(seen.keys()),
                  title="Faculty", loc="upper left", fontsize=10, title_fontsize=10)
ax1.add_artist(leg1)
ax1.legend(handles=size_handles, title="Bubble size", loc="lower left",
           fontsize=9, title_fontsize=9, scatterpoints=1)

# ══════════════════════════════════════════════════════════════════════════
# Panel (b): Power user rate by Faculty (horizontal stacked bar)
# ══════════════════════════════════════════════════════════════════════════
ax2 = fig.add_subplot(gs[0, 1])

pu_fac = (df.groupby(FACULTY_COL)["Power User"]
            .agg(["sum", "count"])
            .reindex(FACULTY_ORDER)
            .fillna(0))
pu_fac.columns = ["PU", "Total"]
pu_fac["Rest"] = pu_fac["Total"] - pu_fac["PU"]
pu_fac["Pct"]  = (pu_fac["PU"] / pu_fac["Total"] * 100).fillna(0)

fac_colors_list = [FAC_COLORS[f] for f in FACULTY_ORDER]
ax2.barh(FACULTY_ORDER, pu_fac["PU"],   color=fac_colors_list, label="Power Users")
ax2.barh(FACULTY_ORDER, pu_fac["Rest"], left=pu_fac["PU"],
         color=fac_colors_list, alpha=0.22, label="Other Users")

for i, (pu, total, pct) in enumerate(zip(pu_fac["PU"], pu_fac["Total"], pu_fac["Pct"])):
    if pu > 0:
        ax2.text(pu / 2, i, f"{int(pu)} ({pct:.0f}%)",
                 ha="center", va="center", fontsize=9, fontweight="bold", color="white")
    ax2.text(total + 0.5, i, f"n={int(total)}", va="center", fontsize=8, color="grey")

ax2.set_xlabel("Respondents", fontsize=10)
ax2.set_xlim(0, pu_fac["Total"].max() * 1.18)
ax2.set_title("(b) Power Users by Faculty\n(5+ days/wk  &  2+ hrs stay)",
              fontweight="bold", fontsize=11)
ax2.legend(fontsize=9, loc="lower right")
ax2.invert_yaxis()
ax2.grid(axis="x", linestyle="--", alpha=0.4)
ax2.set_axisbelow(True)

# ══════════════════════════════════════════════════════════════════════════
# Panel (c): Power user rate by Year of Study
# ══════════════════════════════════════════════════════════════════════════
ax3 = fig.add_subplot(gs[1, 1])

pu_yr = (df.groupby(YEAR_COL)["Power User"]
           .agg(["sum", "count"])
           .reindex(YEAR_ORDER)
           .fillna(0))
pu_yr.columns = ["PU", "Total"]
pu_yr["Rest"] = pu_yr["Total"] - pu_yr["PU"]
pu_yr["Pct"]  = (pu_yr["PU"] / pu_yr["Total"] * 100).fillna(0)

yr_colors_list = [YEAR_COLORS[y] for y in YEAR_ORDER]
ax3.barh(YEAR_ORDER, pu_yr["PU"],   color=yr_colors_list, label="Power Users")
ax3.barh(YEAR_ORDER, pu_yr["Rest"], left=pu_yr["PU"],
         color=yr_colors_list, alpha=0.22, label="Other Users")

for i, (pu, total, pct) in enumerate(zip(pu_yr["PU"], pu_yr["Total"], pu_yr["Pct"])):
    if pu > 0:
        ax3.text(pu / 2, i, f"{int(pu)} ({pct:.0f}%)",
                 ha="center", va="center", fontsize=9, fontweight="bold", color="white")
    ax3.text(total + 0.5, i, f"n={int(total)}", va="center", fontsize=8, color="grey")

ax3.set_xlabel("Respondents", fontsize=10)
ax3.set_xlim(0, pu_yr["Total"].max() * 1.18)
ax3.set_title("(c) Power Users by Year of Study\n(5+ days/wk  &  2+ hrs stay)",
              fontweight="bold", fontsize=11)
ax3.legend(fontsize=9, loc="lower right")
ax3.invert_yaxis()
ax3.grid(axis="x", linestyle="--", alpha=0.4)
ax3.set_axisbelow(True)

# ── Supertitle ─────────────────────────────────────────────────────────────
total_pu = int(df["Power User"].sum())
fig.suptitle(
    f"Power User Identification — Open Area\n"
    f"Defined as: 5+ days/week  AND  planned stay ≥ 2 hours  |  "
    f"Total power users: {total_pu} / {len(df)} ({total_pu/len(df)*100:.1f}%)",
    fontsize=12, fontweight="bold", y=1.02
)

plt.savefig("power_users.png", dpi=150, bbox_inches="tight")
plt.show()

print(f"\nTotal power users: {total_pu} / {len(df)} ({total_pu/len(df)*100:.1f}%)")
print("\nBy Faculty:\n", pu_fac[["PU", "Total", "Pct"]].round(1).to_string())
print("\nBy Year:\n",    pu_yr[["PU",  "Total", "Pct"]].round(1).to_string())
