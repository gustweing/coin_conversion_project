#Trabalharemos com a regra de negócio

from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func 
from sqlalchemy.orm import declarative_base

#Base do SQLalchemy
Base = declarative_base() 

class ProductBase(Base):
    __tablename__ = 'coin_price'
    id_transacao = Column(Integer, primary_key=True)
    moeda_mae = Column(String)
    moeda_filha = Column(String)
    vlr_max_dia = Column(Float)
    vlr_min_dia = Column(Float)
    vlr_cotacao = Column(Float)
    dia_cotacao = Column(DateTime)
    dia_extracao = Column(DateTime(timezone=True), 
                          default=func.now())