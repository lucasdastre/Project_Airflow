from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

SQLALCHEMY_DATABASE_URL = "postgresql://dbname_3e6o_user:yJvpCRJRyKmcSXt2wZk8JBaLavXP6cKV@dpg-d2tkopffte5s73abinqg-a.oregon-postgres.render.com/dbname_3e6o"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()