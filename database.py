from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine("sqlite:///loja.db", echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

def criar_banco():
    Base.metadata.create_all(engine)