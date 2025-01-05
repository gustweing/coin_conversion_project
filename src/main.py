import requests as r
from datetime import datetime

url = 'https://economia.awesomeapi.com.br/json/daily/USD-BRL/10'
response = r.get(url)

try:
    if response.status_code == 200:
        data = response.json()
        dc_data: dict = {}
except:
    print('Não foi possível converter')

