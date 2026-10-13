import pandas as pd
import requests

url = "https://lrangu2.pythonanywhere.com/api/public/"
response = requests.get(url)
payload = response.json()

if payload.get("success"):
    df = pd.DataFrame(payload["data"])
    df['month'] = pd.to_datetime(df['month'])
    df = df.sort_values('month').reset_index(drop=True)
else:
    print("Error fetching data from API")

display(df[['new_users', 'total_users']].describe())

total_months = len(df)
latest_total_users = df['total_users'].iloc[-1]
average_monthly_signups = df['new_users'].mean()

print(f"\nTotal Tracked Months: {total_months}")
print(f"Current Total Community Size: {latest_total_users}")
print(f"Average New Users Per Month: {average_monthly_signups:.2f}")