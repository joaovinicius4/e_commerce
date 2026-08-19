from sqlalchemy import Column, Integer, String, Float
from database import Base

class Produto(Base):
    __tablename__ = 'produtos' 
    id_produto = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)
    preco = Column(Float, nullable=False)
    estoque = Column(Integer, nullable=False)

    def __init__(self, nome: str, preco: float, estoque: int):
        self.nome = nome
        self.preco = preco
        self.estoque = estoque

    def __str__(self) -> str:
        return f"Produto: {self.nome}, Codigo: {self.id_produto}, Preço: R$ {self.preco:.2f}, Quantidade em estoque: {self.estoque}"

    def adicionar_estoque(self, quantidade: int) -> None:
        if quantidade > 0:
            self.estoque += quantidade

    def remover_estoque(self, quantidade: int) -> None:
        if quantidade <= 0:
            raise ValueError("A quantidade a ser removida deve ser maior que zero.")
        
        if quantidade > self.estoque:
            raise ValueError(f"Estoque insuficiente. Disponível: {self.estoque}, solicitado: {quantidade}")
            
        self.estoque -= quantidade