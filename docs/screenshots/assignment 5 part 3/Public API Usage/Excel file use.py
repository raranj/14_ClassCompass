import pandas as pd
import requests

response = requests.get('https://lrangu2.pythonanywhere.com/api/public/')
payload = response.json()

if payload.get('success'):
  df = pd.DataFrame(payload['data'])
  df.to_excel('community_growth.xlsx', index=False)
  print('Excel file generated successfully!')