#Criando o banco de dados

from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker, declarative_base

SQLITE_DECLARATIVE_URL = "sqlite:///./coinbase.sqlite"

engine = create_engine(SQLITE_DECLARATIVE_URL) #Estou utilizando SQLite para quem desejar rodar, conseguir 
#sem problemas de acesso a bancos. 
Sessionlocal = sessionmaker(
    autocommit = False, 
    autoflush = False, 
    bind = engine
)
