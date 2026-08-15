from datetime import datetime
from entities import Carrinho

class Pedido:
    def __init__(self, carrinho: Carrinho, id_pedido: int):
        self.id_pedido = id_pedido
        self.itens = list(carrinho.itens)
        self.valor_total = carrinho.calcular_total()
        self.data_pedido = datetime.now()
        self.status = "PENDENTE"

    def confirmar_pedido(self):
        if self.status != "PENDENTE":
            print("Este pedido já foi processado anteriormente.")
            return

        for item in self.itens:
            produto = item['produto']
            quantidade = item['quantidade']
            if quantidade > produto.estoque:
                raise ValueError(f"Estoque insuficiente para {produto.nome} no momento da confirmação!")

        for item in self.itens:
            item["produto"].remover_estoque(item['quantidade'])

        self.status = "APROVADO"

        print(f"Pedido #{self.id_pedido} confirmado com sucesso! Estoque debitado.")

    def __str__(self) -> str:
        data_formatada = self.data_pedido.strftime('%d/%m/%Y %H:%M')
        return f"Pedido #{self.id_pedido} | Data: {data_formatada} | Status: {self.status} | Total: R$ {self.valor_total:.2f}"

        
        