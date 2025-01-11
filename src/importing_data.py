import requests as r
import pandas as pd
from schema import ProductUpdate  # Modelo Pydantic para validação de dados
from pydantic import ValidationError
from models import ProductBase  # Modelo SQLAlchemy para persistência no banco
from sqlalchemy.orm import Session
from database import Sessionlocal  # Sessão do banco de dados configurada com SQLAlchemy
import json


def geracao_dados(lista_moedas: list, num_dias: int):
    """
    Gera os dados das cotações das moedas para o número de dias especificado.
    """
    filtrados = []
    # Gerar combinações de moedas mãe e filha
    pares_moedas = [
        (mae, filha) for mae in lista_moedas for filha in lista_moedas if mae != filha
    ]
    for mae, filha in pares_moedas:
        url = f'https://economia.awesomeapi.com.br/json/daily/{mae}-{filha}/{num_dias}'
        try:
            response = r.get(url, timeout=10)  # Timeout para evitar travamento
            if response.status_code == 200:
                try:
                    data = response.json()
                    for item in data:
                        filtrados.append({
                            'code': item.get('code', mae),
                            'codein': item.get('codein', filha),
                            'max': item.get('high', 'n/a'),
                            'min': item.get('low', 'n/a'),
                            'bid': item.get('bid', 'n/a'),
                            'time': item.get('timestamp', 'n/a'),
                        })
                except json.JSONDecodeError as e:
                    print(f"Erro ao decodificar JSON para {mae}-{filha}: {e}")
            else:
                print(f"Erro HTTP {response.status_code} para {mae}-{filha}")
        except (r.RequestException, Exception) as e:
            print(f"Erro ao acessar a URL {url}: {e}")
    return filtrados


def ajustes_dados(filtrados):
    """
    Ajusta os dados coletados, realiza limpeza e converte timestamps.
    """
    df = pd.DataFrame(filtrados)
    if df.empty:
        print("Nenhum dado foi coletado para ajuste.")
        return []

    # Limpeza de caracteres indesejados
    df['code'] = df['code'].str.replace(r"[{}']", "", regex=True)
    df['codein'] = df['codein'].str.replace(r"[{}']", "", regex=True)
    # Conversão de timestamps para data normalizada
    df['time'] = pd.to_datetime(df['time'], unit='s', errors='coerce').dt.normalize()

    return df.to_dict(orient='records')  # Retorna lista de dicionários


def carregar_importar_dados(data):
    """
    Insere os dados ajustados no banco de dados usando SQLAlchemy.
    """
    db: Session = Sessionlocal()

    try:
        registros_validos = []
        for item in data:
            try:
                validated_data = ProductUpdate(**item)  # Validação Pydantic
                # Preparar o modelo para inserção no banco
                registros_validos.append(ProductBase(
                    moeda_mae=validated_data.code,
                    moeda_filha=validated_data.codein,
                    vlr_max_dia=validated_data.max,
                    vlr_min_dia=validated_data.min,
                    vlr_cotacao=validated_data.bid,
                    dia_cotacao=validated_data.time
                ))
            except ValidationError as e:
                print(f"Erro de validação para {item}: {e}")

        if registros_validos:
            db.bulk_save_objects(registros_validos)  # Inserção em lote
            db.commit()
            print(f"{len(registros_validos)} registros inseridos com sucesso!")
        else:
            print("Nenhum registro válido encontrado para inserção.")
    except Exception as e:
        db.rollback()
        print(f"Erro ao inserir dados no banco: {e}")
    finally:
        db.close()
