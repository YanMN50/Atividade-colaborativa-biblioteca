import os
from sqlalchemy import create_engine, Column, String, Integer, Float
from sqlalchemy.orm import sessionmaker, declarative_base
from dataclasses import dataclass

db = create_engine("sqlite:///meubanco.db")

Session = sessionmaker(bind=db)
session = Session()


Base = declarative_base()

class Cliente(Base):
    __tablename__ = "clientes"

    matricula = Column(Integer, primary_key=True)
    nome = Column(String)
    email = Column(String)
    senha = Column(String)

    def __init__(self, matricula:int, nome:str, email:str, senha:str):
        self.matricula = matricula
        self.nome = nome
        self.email = email
        self.senha = senha


Base.metadata.create_all(bind=db)

os.system("cls || clear")

