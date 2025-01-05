import requests as r
from datetime import datetime

moedas = [
'USD-BRL',
'CAD-BRL',
'EUR-BRL',
'GBP-BRL',
'ARS-BRL',
'BTC-BRL',
'LTC-BRL',
'JPY-BRL',
'CHF-BRL',
'AUD-BRL',
'CNY-BRL',
'ILS-BRL',
'ETH-BRL',
'XRP-BRL'     
]   

datestart = 20240501 
dateend = 20240505
filtrados: list = []
for i in moedas:
    url = f'https://economia.awesomeapi.com.br/json/daily/{i}/?start_date={datestart}&end_date={dateend}'
    response = r.get(url)

    if response.status_code == 200:
            data = response.json()
    else:
        print(f'Não foi possível converter devido ao erro {response.status_code}')
        exit()

    for lista in data:
        filtrados.append({
            'code': lista.get('code','n/a'), 
            'codein':lista.get('codein','n/a'), 
            'max':lista.get('high','n/a'),
            'min': lista.get('low','n/a'), 
            'bid': lista.get('bid','n/a'), 
            'time': lista.get('timestamp','n/a')
        })

print(filtrados)    