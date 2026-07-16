import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

df = pd.read_csv("intervalDataRemoveOther.csv")

INTERVAL_ORDER = ["Morning", "Midday", "Afternoon", "Evening"]
METRICS = {
    "Thermal Comfort":            {"color": "#E74C3C", "marker": "o",  "ls": "-"},
    "Noise Level":                {"color": "#E67E22", "marker": "s",  "ls": "--"},
    "Occupancy Level":            {"color": "#8172B2", "marker": "^",  "ls": "-."},
    "Weather Conditions(Rain/Breeze)": {"color": "#2980B9", "marker": "D",  "ls": ":"},
}

# Compute means per interval (preserve order)
df["Interval"] = pd.Categorical(df["Interval"], categories=INTERVAL_ORDER, ordered=True)
means = df.groupby("Interval", observed=True)[list(METRICS.keys())].mean().reindex(INTERVAL_ORDER)

# ── Figure ──────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(10, 6))

x = np.arange(len(INTERVAL_ORDER))

for metric, style in METRICS.items():
    y = means[metric].values
    ax.plot(x, y, color=style["color"], marker=style["marker"],
            linestyle=style["ls"], linewidth=2.2, markersize=8,
            label=metric, zorder=3)
    # Annotate each point with its mean value
    for xi, yi in zip(x, y):
        ax.annotate(
            f"{yi:.2f}",
            xy=(xi, yi),
            xytext=(0, 10),
            textcoords="offset points",
            ha="center", fontsize=9,
            color=style["color"], fontweight="bold"
        )

# ── Shade the degradation zone (Midday) ─────────────────────────────────────
ax.axvspan(0.5, 1.5, alpha=0.08, color="#E74C3C", label="Peak degradation zone")

# ── Styling ──────────────────────────────────────────────────────────────────
ax.set_xticks(x)
ax.set_xticklabels(INTERVAL_ORDER, fontsize=12)
ax.set_ylim(0.5, 5.5)
ax.yaxis.set_major_locator(ticker.MultipleLocator(1))
ax.set_yticks([1, 2, 3, 4, 5])
ax.set_yticklabels(["1\n(Very Low)", "2", "3\n(Moderate)", "4", "5\n(Very High)"], fontsize=9)

ax.set_xlabel("Time of Day", fontsize=12)
ax.set_ylabel("Mean Score (1 – 5 scale)", fontsize=12)
ax.set_title(
    "Diurnal Thermal and Auditory Degradation Curve\n"
    "Mean Comfort Scores Across Operational Time Blocks",
    fontsize=13, fontweight="bold", pad=14
)

ax.grid(axis="y", linestyle="--", linewidth=0.6, alpha=0.5)
ax.set_axisbelow(True)

legend = ax.legend(
    title="Metric", loc="upper right",
    fontsize=10, title_fontsize=10,
    framealpha=0.9
)

plt.tight_layout()
plt.savefig("trend_a_diurnal_degradation.png", dpi=150, bbox_inches="tight")
plt.show()

print("Chart saved as trend_a_diurnal_degradation.png")
print("\nMean scores per interval:")
print(means.round(2).to_string())
