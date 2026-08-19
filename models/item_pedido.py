from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class ItemPedido(Base):
    __tablename__ = 'itens_pedido'
    
    id_item = Column(Integer, primary_key=True, autoincrement=True)
    pedido_id = Column(Integer, ForeignKey('pedidos.id_pedido'), nullable=False)
    produto_id = Column(Integer, ForeignKey('produtos.id_produto'), nullable=False)
    quantidade = Column(Integer, nullable=False)
    preco_unitario = Column(Float, nullable=False)

    produto = relationship("Produto")