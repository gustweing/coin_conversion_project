import requests as r

url = 'https://economia.awesomeapi.com.br/json/daily/USD-BRL/30'
response = r.get(url)

try:
    if response.status_code == 200:
        data = response.json()
        print(data)
except:
    print('Não foi possível converter')


