import pandas as pd
from auxiliares import *
from datetime import datetime, timedelta
from models import ProductCliente, ProductOptions
from database import Sessionlocal
from sqlalchemy.orm import Session
import random

def gerar_datas_aleatorias(data_inicio, data_fim):
    delta = data_fim - data_inicio
    int_delta = delta.days
    random_days = random.randrange(int_delta)
    return data_inicio + timedelta(days=random_days)

def num_linhas():
    qtd = random.randint(6000,8000)
    return qtd

def gerar_clientes():

    moedas = ['BRL', 'USD', 'CAD', 'EUR', 'GBP', 'ARS', 'JPY', 'CHF', 'AUD', 'CNY', 'ILS']
    #Criar as empresas
    num_empresas = random.randint(90, 150)
    #Dicionario nome + moeda usada
    empresas_moeda = {}
    for l in range(1,num_empresas):
        nome_empresa = f'Empresa {l}'
        moeda = random.choice(moedas)
        empresas_moeda[nome_empresa] = moeda
    return empresas_moeda

def gerar_tabela(empresas_moeda):
    
    linhas = num_linhas()
    inicio = datetime(2024,6,16)
    fim = datetime(2025,1,10)
    acoes = [1,2] #1 compra 2 venda

    dados = []

    for i in range(linhas):
        nome_empresa, moeda = random.choice(list(empresas_moeda.items()))
        valor = round(random.randint(1,100))
        dia_acao = gerar_datas_aleatorias(inicio,fim).strftime('%Y-%m-%d')
        acao = random.choice(acoes)

        dados.append(
            [nome_empresa, 
             moeda, 
             valor,
             dia_acao, 
             acao])

    #criar um dataframe dos dados
    df = pd.DataFrame(
        dados, 
        columns= ['nome_empresa', 'moeda', 'quantidade', 'dia' , 'tipo_operacao']
    )

    return df

def ingestao_fato():
    clientes = gerar_clientes()
    df = gerar_tabela(clientes)
    db: Session = Sessionlocal()  
    for _, row in df.iterrows():
        cadastro = ProductOptions(
            nome_empresa = row['nome_empresa'],
            moeda = row['moeda'],
            acao = row['tipo_operacao'], 
            valor_acao = ['quantidade'],
            dia_acao = row['dia']
        ) 
        db.add(cadastro)
        db.commit()
        db.close()

def ingestao_clientes():
    empresas_moeda = gerar_clientes()
    db: Session = Sessionlocal()

    df_empresas = pd.DataFrame(empresas_moeda)
    for _, row in df_empresas.iterrows():
        cadastro = ProductCliente(
            nome_empresa = row['nome_empresa'],
            moeda_empresa = row['moeda']
        ) 
        db.add(cadastro)
        db.commit()
        db.close()