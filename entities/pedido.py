from datetime import datetime
from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from entities.item_pedido import ItemPedido
from database import Base
from services.carrinho import Carrinho

class Pedido(Base):
    __tablename__ = 'pedidos'

    id_pedido = Column(Integer, primary_key=True, autoincrement=True)
    valor_total = Column(Float, nullable=False)
    data_pedido = Column(DateTime, default=datetime.now)
    status = Column(String(20), default="PENDENTE")
    
    cliente_id = Column(Integer, ForeignKey('clientes.id_cliente'), nullable=False)
    cliente = relationship("Cliente")
    
    itens = relationship("ItemPedido", cascade="all, delete-orphan")

    def __init__(self, carrinho, cliente):
        self.cliente = cliente
        self.valor_total = carrinho.calcular_total()
        self.data_pedido = datetime.now()
        self.status = "PENDENTE"
        
        self.itens = []
        for item_carrinho in carrinho.itens:
            produto = item_carrinho['produto']
            quantidade = item_carrinho['quantidade'] 
            novo_item = ItemPedido(
                produto=produto,
                quantidade=quantidade,
                preco_unitario=produto.preco
            )
            self.itens.append(novo_item)

    def confirmar_pedido(self):
        if self.status != "PENDENTE":
            print("Este pedido já foi processado anteriormente.")
            return
        for item in self.itens:
            produto = item.produto
            if item.quantidade > produto.estoque:
                raise ValueError(f"Estoque insuficiente para {produto.nome} no momento da confirmação!")
            produto.remover_estoque(item.quantidade)
        self.status = "APROVADO"
        print(f"Pedido #{self.id_pedido} confirmado com sucesso! Estoque debitado.")

    def __str__(self) -> str:
        data_formatada = self.data_pedido.strftime('%d/%m/%Y %H:%M')
        nome_cliente = self.cliente.nome if self.cliente else "Desconhecido"
        return f"Pedido #{self.id_pedido} | Cliente: {nome_cliente} | Data: {data_formatada} | Status: {self.status} | Total: R$ {self.valor_total:.2f}"