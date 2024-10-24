import os
from sqlalchemy import create_engine, Column, String, Integer, Float
from sqlalchemy.orm import sessionmaker, declarative_base
from dataclasses import dataclass

db = create_engine("sqlite:///meubanco.db")

