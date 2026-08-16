from sqlalchemy import Column, Integer, String
from database import Base

class Cliente(Base):
    __tablename__ = 'clientes'

    id_cliente = Column(Integer, primary_key=True, autoincrement=True)
    cpf = Column(String(11), unique=True, nullable=False)           
    nome = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    endereco = Column(String(100), nullable=False)

    def __init__(self, cpf: str, nome: str, email: str, endereco: str):
        self.cpf = cpf
        self.nome = nome
        self.email = email
        self.endereco = endereco

    def __str__(self) -> str:
        return f"Cliente: {self.nome} | CPF: {self.cpf} | E-mail: {self.email}"