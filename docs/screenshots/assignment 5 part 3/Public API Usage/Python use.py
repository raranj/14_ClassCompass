import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests

url = "https://lrangu2.pythonanywhere.com/api/public/"

try:
    response = requests.get(url)
    response.raise_for_status()
    payload = response.json()

    if not payload.get("success"):
        print("API returned an unsuccessful state.")
        exit()
    df = pd.DataFrame(payload["data"])
    df["month"] = pd.to_datetime(df["month"])
    df = df.sort_values("month").reset_index(drop=True)
    x_dates = df["month"]
    x_numeric = mdates.date2num(x_dates)
    y = df["total_users"]

    slope, intercept = np.polyfit(x_numeric, y, 1)
    y_fit = slope * x_numeric + intercept

    plt.figure(figsize=(10, 5))
    plt.scatter(
        x_dates,
        y,
        color="#2563eb",
        s=100,
        zorder=3,
        label="Actual New Users",
    )
    plt.plot(
        x_dates,
        y_fit,
        color="#dc2626",
        linestyle="--",
        linewidth=2,
        label="Trend Line (Line of Best Fit)",
    )
    plt.title("Community Growth Scatter Plot & Trend Line", fontsize=14, fontweight="bold")
    plt.xlabel("Month", fontsize=12)
    plt.ylabel("New Users", fontsize=12)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
    plt.gcf().autofmt_xdate()
    plt.grid(True, linestyle=":", alpha=0.6)
    plt.legend()
    plt.tight_layout()
    plt.show()
except Exception as error:
    print(f"An error occurred: {error}")

