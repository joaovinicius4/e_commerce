from datetime import datetime
from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from models.item_pedido import ItemPedido
from database import Base

class Pedido(Base):
    __tablename__ = 'pedidos'
    id_pedido = Column(Integer, primary_key=True, autoincrement=True)
    valor_total = Column(Float, nullable=False)
    data_pedido = Column(DateTime, default=datetime.now)
    status = Column(String(30), default="PENDENTE") # PENDENTE, PAGO, CANCELADO, etc.
    
    cliente_id = Column(Integer, ForeignKey('clientes.id_cliente'), nullable=False)
    cliente = relationship("Cliente")
    itens = relationship("ItemPedido", cascade="all, delete-orphan")

    def __init__(self, cliente, valor_total, itens_carrinho):
        self.cliente = cliente
        self.valor_total = valor_total
        self.data_pedido = datetime.now()
        self.status = "PENDENTE"
        self.itens = []
        for item_carrinho in itens_carrinho:
            produto = item_carrinho['produto']
            quantidade = item_carrinho['quantidade'] 
            novo_item = ItemPedido(
                produto=produto,
                quantidade=quantidade,
                preco_unitario=produto.preco
            )
            self.itens.append(novo_item)

    def validar_e_baixar_estoque(self):
        for item in self.itens:
            produto = item.produto
            if item.quantidade > produto.estoque:
                raise ValueError(f"Estoque insuficiente para o produto: {produto.nome} (Disponível: {produto.estoque})")
            produto.estoque -= item.quantidade

    def __str__(self) -> str:
        data_formatada = self.data_pedido.strftime('%d/%m/%Y %H:%M')
        nome_cliente = self.cliente.nome if self.cliente else "Desconhecido"
        return f"Pedido #{self.id_pedido} | Cliente: {nome_cliente} | Data: {data_formatada} | Status: {self.status} | Total: R$ {self.valor_total:.2f}"