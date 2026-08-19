from datetime import datetime
from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Pagamento(Base):
    __tablename__ = "pagamentos"
    id_pagamento = Column(Integer, primary_key=True, autoincrement=True)
    pedido_id = Column(
        Integer,
        ForeignKey("pedidos.id_pedido"),
        nullable=False
    )

    forma_pagamento = Column(String(20), nullable=False)
    status = Column(String(30), default="PENDENTE")
    valor = Column(Float, nullable=False)
    codigo_transacao = Column(String(100), nullable=True)
    data_pagamento = Column(DateTime, default=datetime.now)

    pedido = relationship("Pedido")