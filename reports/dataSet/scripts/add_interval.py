import pandas as pd
from dateutil import parser as dateparser

def get_interval(ts_str):
    try:
        dt = dateparser.parse(str(ts_str))
        hour = dt.hour + dt.minute / 60
        if 7 <= hour < 11:
            return "Morning"
        elif 11 <= hour < 13:
            return "Midday"
        elif 13 <= hour < 16:
            return "Afternoon"
        elif 16 <= hour < 19:
            return "Evening"
        else:
            return "Other"
    except Exception:
        return "Unknown"

df = pd.read_csv("clnData.csv")

df.insert(0, "Interval", df["Timestamp"].apply(get_interval))
df.drop(columns=["Timestamp"], inplace=True)

df.to_csv("intervalData.csv", index=False)
print(f"Saved intervalData.csv with {len(df)} rows.")
print(df["Interval"].value_counts())
