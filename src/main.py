import requests as r
from datetime import datetime
import time

moeda_mae =['BRL',
'USD',
'CAD',
'EUR',
'GBP',
'ARS',
'BTC',
'LTC',
'JPY',
'CHF',
'AUD',
'CNY',
'ILS',
'ETH',
'XRP' ]
moedas_secundaria = [
'BRL',
'USD',
'CAD',
'EUR',
'GBP',
'ARS',
'BTC',
'LTC',
'JPY',
'CHF',
'AUD',
'CNY',
'ILS',
'ETH',
'XRP'    
]

j = 0
num_dias = 2
filtrados: list = []

for mae in moeda_mae:
    for i in moedas_secundaria:
        url = f'https://economia.awesomeapi.com.br/json/daily/{mae}-{i}/{num_dias}'
        response = r.get(url)

        try:
            if response.status_code == 200:
                data = response.json()
    
                for lista in data:
                    filtrados.append({
                        'code': lista.get('code',{mae}), 
                        'codein':lista.get('codein',{i}), 
                        'max':lista.get('high','n/a'),
                        'min': lista.get('low','n/a'), 
                        'bid': lista.get('bid','n/a'), 
                        'time': lista.get('timestamp','n/a')
                    })
        except:
            print(f'Não foi possível converter devido ao erro {response.status_code}')
            print(f'Erro ao processar a moeda {i}.')
        
print(filtrados)


    