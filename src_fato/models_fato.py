#Trabalharemos com a regra de negócio

from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.sql import func 
from sqlalchemy.orm import declarative_base

#Base do SQLalchemy
Base = declarative_base() 

class ProductOptions(Base):
    __tablename__ = 'coins_options'
    id_transacao = Column(Integer, primary_key=True)
    id_cliente = Column(Integer, nullable=False)
    moeda = Column(String, nullable=False)
    acao = Column(String, nullable=False)
    valor_acao = Column(Float, nullable=False)
    dia_acao = Column(Date,nullable=False)


class ProductCliente(Base):
    __tablename__ = 'clients'
    id_cliente = Column(Integer, primary_key=True)
    nome_empresa = Column(String, nullable=False)
    moeda_empresa = Column(String, nullable=False)
