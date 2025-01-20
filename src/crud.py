from database import engine 
from models import Base
from importing_data import geracao_dados, ajustes_dados, carregar_importar_dados
from auxiliares import LISTA_MOEDAS

def init_db():
    Base.metadata.create_all(bind=engine) 

def imports():
    print("Iniciando coleta de dados...")
    data = geracao_dados(LISTA_MOEDAS,180)
    print(f"Dados coletados: {len(data)} registros.")
    print("Ajustando dados...")
    data = ajustes_dados(data)
    if data:
        print("Carregando dados no banco...")
        carregar_importar_dados(data)
    else:
        print("Nenhum dado ajustado para carregar no banco.")
