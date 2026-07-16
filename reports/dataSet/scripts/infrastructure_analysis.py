import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import re

# Load data
df = pd.read_csv("intervalDataRemoveOther.csv")
N = len(df)

# ═══════════════════════════════════════════════════════════════════════════
# Helper: horizontal bar with % labels (Fixed text padding)
# ═══════════════════════════════════════════════════════════════════════════
def hbar(ax, series, colors, title, xlabel="Respondents (n)", pct=True):
    bars = ax.barh(series.index, series.values, color=colors,
                   edgecolor="white", linewidth=0.5)
    
    # Dynamically calculate padding based on the maximum value in the series
    # to prevent text from crowding the bar edges
    x_padding = max(series.max() * 0.02, 0.3)
    
    for bar, val in zip(bars, series.values):
        pct_str = f"  {val}  ({val/N*100:.1f}%)" if pct else f"  {val}"
        ax.text(val + x_padding, bar.get_y() + bar.get_height() / 2,
                pct_str, va="center", fontsize=8.5, color="#333333")
        
    ax.set_xlabel(xlabel, fontsize=9)
    ax.set_title(title, fontweight="bold", fontsize=10, pad=8)
    ax.set_xlim(0, max(series.max() * 1.35, 5))
    ax.grid(axis="x", linestyle="--", alpha=0.4)
    ax.set_axisbelow(True)
    ax.tick_params(axis="y", labelsize=9)
    ax.invert_yaxis()

# ═══════════════════════════════════════════════════════════════════════════
# Data Extraction & Mapping
# ═══════════════════════════════════════════════════════════════════════════
def _map(x, mapping):
    s = str(x).lower()
    for k, v in mapping:
        if k in s:
            return v
    return "Other"

# 1. Pull Factors
REASON_COL = "What are the top reasons you chose to sit here today?"
REASONS = [
    ("Availability of power plugs",   "Power Plugs Availability"),
    ("Wi-Fi/Signal strength",         "Wi-Fi / Signal Strength"),
    ("Large seating space",           "Large Seating Space"),
    ("To meet up with friends",       "To Meet Up with Friends"),
    ("Proximity to faculty/lectures", "Proximity to Faculty/Lectures"),
    ("Atmosphere/Vibe",               "Atmosphere / Vibe"),
]
reason_counts = {label: df[REASON_COL].str.contains(re.escape(pat), na=False).sum() for pat, label in REASONS}
reason_s = pd.Series(reason_counts).sort_values()

# 2. Fan Impact
FAN_COL = "To what extent would the installation of ceiling/wall fans change your usage of the Open Area during warm periods?"
fan_map = [
    ("not affect",                  "No change to usage"),
    ("more comfortable",            "More comfortable\n(same duration)"),
    ("instead of going elsewhere",  "Would choose space\nover alternatives"),
    ("significantly increase",      "Significantly more\ntime spent here"),
]
df["Fan Impact"] = df[FAN_COL].apply(_map, mapping=fan_map)
fan_order = [v for _, v in fan_map]
fan_vc = df["Fan Impact"].value_counts().reindex(fan_order, fill_value=0)

# 3. Power Dependency
POWER_COL = "Are you currently using an electronic device (laptop/phone/tablet) that requires a continuous power supply to stay here?"
power_map = [
    ("plugged into a wall", "Plugged into wall socket"),
    ("running on battery",  "Device on battery only"),
    ("No",                  "No device / no power need"),
]
df["Power Status"] = df[POWER_COL].apply(_map, mapping=power_map)
power_order = [v for _, v in power_map]
power_vc = df["Power Status"].value_counts().reindex(power_order, fill_value=0)

# 4. Rain Impact
RAIN_COL = "How does rainy weather typically affect your choice to use the Open Area?"
rain_map = [
    ("doesn't affect",       "No impact\n(use it regardless)"),
    ("wait or seek shelter", "Shelter / passive use\n(wait for rain to stop)"),
    ("avoid",                "Avoid entirely\n(dampness / splashing)"),
]
df["Rain Impact"] = df[RAIN_COL].apply(_map, mapping=rain_map)
rain_order = [v for _, v in rain_map]
rain_vc = df["Rain Impact"].value_counts().reindex(rain_order, fill_value=0)

# 5. Noise Sensitivity
NOISE_COL = "If this space became significantly louder right now due to a social event what would you do?"
noise_map = [
    ("tolerate the noise",   "Stay & tolerate noise"),
    ("switch to casual",     "Stay & switch to casual/phone"),
    ("move if it gets",      "Stay but relocate\nif too distracting"),
    ("another building",     "Leave to another\nbuilding"),
]
df["Noise Response"] = df[NOISE_COL].apply(_map, mapping=noise_map)
noise_order = [v for _, v in noise_map]
noise_vc = df["Noise Response"].value_counts().reindex(noise_order, fill_value=0)

# 6. Suggestions
SUGGEST_COL = "Any suggestions to improve infrastructure of the area?"
suggest_patterns = [
    (r"fan|ventilat",            "Fans / Ventilation"),
    (r"curtain|rain.shield",     "Curtains / Rain Shields"),
    (r"chair|seat|furniture|back|backbone", "Seating / Furniture"),
    (r"wifi|wi.fi|network|signal",          "Wi-Fi / Connectivity"),
    (r"plug|power|socket",                  "Power Plugs / Sockets"),
]
suggest_counts = {label: df[SUGGEST_COL].str.contains(pat, case=False, na=False, regex=True).sum() for pat, label in suggest_patterns}
suggest_s = pd.Series(suggest_counts).sort_values()

# ═══════════════════════════════════════════════════════════════════════════
# FIGURE SETUP (Fixed Spacing & Layout Parameters)
# ═══════════════════════════════════════════════════════════════════════════
# 1. Increased width from 18 to 20 to give horizontal elements more breathing room.
fig = plt.figure(figsize=(20, 17)) 

# 2. Significantly increased wspace from 0.42 to 0.78 to prevent column overlapping.
# 3. Slightly increased hspace from 0.60 to 0.68 to give titles clean clearance.
gs = gridspec.GridSpec(3, 3, figure=fig,
                       hspace=0.68, wspace=0.78,
                       height_ratios=[1, 1, 1])

# Color Palettes
BLUE_GRAD   = ["#BDD7EE", "#6BAED6", "#2171B5", "#08306B", "#03243a", "#011526"]
FAN_COLORS  = ["#D5E8D4", "#82B366", "#FF8C00", "#C00000"]
PWR_COLORS  = ["#C0392B", "#E67E22", "#27AE60"]
RAIN_COLORS = ["#AED6F1", "#5DADE2", "#154360"]
NOISE_COLORS= ["#D2B4DE", "#A569BD", "#7D3C98", "#4A235A", "#1A0533"]
SUG_COLORS  = ["#FADBD8", "#F1948A", "#E74C3C", "#C0392B", "#7B241C"]

# (a) Infrastructure pull factors — top, full width
ax_a = fig.add_subplot(gs[0, :])
hbar(ax_a, reason_s, BLUE_GRAD[:len(reason_s)],
     "(a)  Infrastructure Pull Factors\nFrequency of reasons cited for choosing the Open Area")

# (b) Fan installation impact — middle left
ax_b = fig.add_subplot(gs[1, 0])
hbar(ax_b, fan_vc, FAN_COLORS,
     "(b)  Fan Installation Impact\nWould ceiling/wall fans change usage?")

# (c) Power supply dependency — middle centre
ax_c = fig.add_subplot(gs[1, 1])
hbar(ax_c, power_vc, PWR_COLORS,
     "(c)  Power Supply Dependency\nDevice & power usage status")

# (d) Rainy weather impact — middle right
ax_d = fig.add_subplot(gs[1, 2])
hbar(ax_d, rain_vc, RAIN_COLORS,
     "(d)  Rainy Weather Impact\nHow rain affects Open Area usage")

# (e) Noise sensitivity — bottom left + centre
ax_e = fig.add_subplot(gs[2, :2])
hbar(ax_e, noise_vc, NOISE_COLORS,
     "(e)  Noise Sensitivity\nResponse to a sudden loud social event in the space")

# (f) Infrastructure suggestions — bottom right
ax_f = fig.add_subplot(gs[2, 2])
hbar(ax_f, suggest_s, SUG_COLORS[:len(suggest_s)],
     "(f)  Suggested Infrastructure Improvements\nKeyword frequency in open-text responses")

fig.suptitle(
    "Infrastructure Analysis — UCSC Open Area\n"
    f"Based on n = {N} survey responses",
    fontsize=14, fontweight="bold", y=0.96
)

# Using bbox_inches="tight" ensures no labels outside the main canvas bounds get clipped
plt.savefig("infrastructure_analysis.png", dpi=150, bbox_inches="tight")
plt.show()

print("Chart saved successfully without overlaps → infrastructure_analysis.png")