import requests
import os
import dotenv

dotenv.load_dotenv()
data = {}
try:
    req = requests.get('https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies/usd.json')
    if req.status_code == 200:
            data.update(req.json())
    print(data['usd'])
except Exception as e:
    print('error',e)