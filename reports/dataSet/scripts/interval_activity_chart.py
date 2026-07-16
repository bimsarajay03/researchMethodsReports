import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("intervalDataRemoveOther.csv")

ACT_COL = "What activities are you doing in the Open Area today?"
INTERVAL_ORDER = ["Morning", "Midday", "Afternoon", "Evening"]

ACTIVITY_LABELS = [
    "Individual Academic Work",
    "Collaborative Academic Work (Group)",
    "Casual Socializing / Chatting",
    "Recreation",
    "University Club Activity",
]

def extract_activities(act_str):
    s = str(act_str)
    found = []
    if "Individual Academic Work" in s:
        found.append("Individual Academic Work")
    if "Collaborative Academic Work" in s:
        found.append("Collaborative Academic Work (Group)")
    if "Casual Socializing" in s:
        found.append("Casual Socializing / Chatting")
    if "Recreation" in s:
        found.append("Recreation")
    if "University Club" in s:
        found.append("University Club Activity")
    return found if found else ["Other"]

# Build count matrix: rows = intervals, columns = activities
counts = pd.DataFrame(0, index=INTERVAL_ORDER, columns=ACTIVITY_LABELS)

for _, row in df.iterrows():
    interval = row["Interval"]
    if interval not in INTERVAL_ORDER:
        continue
    for act in extract_activities(row[ACT_COL]):
        if act in counts.columns:
            counts.loc[interval, act] += 1

# Convert counts to percentages per interval
row_totals = counts.sum(axis=1)
pct = counts.div(row_totals, axis=0) * 100

# --- Stacked Bar Chart ---
COLORS = ["#4C72B0", "#55A868", "#C44E52", "#8172B2", "#CCB974"]

fig, ax = plt.subplots(figsize=(11, 6))
bottom = [0.0] * len(INTERVAL_ORDER)

for i, act in enumerate(ACTIVITY_LABELS):
    values = pct[act].tolist()
    ax.bar(
        INTERVAL_ORDER, values,
        bottom=bottom,
        label=act,
        color=COLORS[i],
        edgecolor="white",
        linewidth=0.6,
    )
    # Add percentage labels inside bars
    for j, (val, bot) in enumerate(zip(values, bottom)):
        if val >= 3:  # only label if segment is large enough to read
            ax.text(
                j, bot + val / 2, f"{val:.1f}%",
                ha="center", va="center",
                fontsize=9, color="white", fontweight="bold"
            )
    bottom = [b + v for b, v in zip(bottom, values)]

ax.set_xlabel("Time of Day", fontsize=12)
ax.set_ylabel("Percentage of Responses (%)", fontsize=12)
ax.set_title("Activities Performed in the Open Area by Time of Day", fontsize=14, fontweight="bold")
ax.legend(title="Activity Type", bbox_to_anchor=(1.02, 1), loc="upper left", fontsize=9)
ax.set_ylim(0, 110)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{x:.0f}%"))
plt.xticks(fontsize=11)
plt.tight_layout()
plt.savefig("interval_vs_activity.png", dpi=150, bbox_inches="tight")
plt.show()
print("Chart saved as interval_vs_activity.png")
print("\nCounts:\n", counts)
