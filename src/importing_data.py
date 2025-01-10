import requests as r
import pandas as pd
from schema import ProductUpdate
from pydantic import ValidationError
from models import ProductBase
from sqlalchemy.orm import Session
from database import Sessionlocal
import json


def geracao_dados(lista_moedas:list,num_dias:int):
    filtrados: list = []
    for mae in lista_moedas:
        for i in lista_moedas:
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

    return filtrados 

def ajustes_dados(filtrados):
    df = pd.DataFrame(filtrados)
    df['code'] = df['code'].str.replace(r"[{}']", "", regex=True)
    df['codein'] = df['codein'].str.replace(r"[{}']", "", regex=True)
    df['time'] = (pd.to_datetime(df['time'], unit = 's')).dt.normalize()
    json_data = df.to_json(orient='records')
    return json_data

def carregar_importar_dados(json_data):
    data = json.loads(json_data)

    db: Session = Sessionlocal()

    try:
        for item in data:
            try: 
                validated_data = ProductUpdate(**item)
            except ValidationError as e:
                print(f'Erro de validação para o {item}: {e}')
                continue

            cadastro = ProductBase(
                moeda_mae = validated_data.code,
                moeda_filha = validated_data.codein, 
                vlr_max_dia = validated_data.max,
                vlr_min_dia = validated_data.min, 
                vlr_cotacao = validated_data.bid, 
                dia_cotacao = validated_data.time
            )
            db.add(cadastro)
        
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Erro ao inserir dados: {e}")
    finally:
        db.close()