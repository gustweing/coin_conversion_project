from database import engine 
from models import Base
from importing_data import geracao_dados, ajustes_dados, carregar_importar_dados
from imports import LISTA_MOEDAS

def init_db():
    Base.metadata.create_all(bind=engine) 

def imports():
    data = geracao_dados(LISTA_MOEDAS,1)
    data = ajustes_dados(data)
    carregar_importar_dados(data)