#Criando o banco de dados

from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker, declarative_base
from imports import *

engine = create_engine(POSTGRESS_DECLARATIVE_URL) #Change here for your database. I'm using POSTGRESQL, but you can use another one. 
Sessionlocal = sessionmaker(
    autocommit = False, 
    autoflush = False, 
    bind = engine
)
