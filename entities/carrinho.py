from entities.produto import Produto


class Carrinho:
    def __init__(self):
        self.itens = []

    def adicionar_produto(self, produto: Produto, quantidade: int) -> None:
        if quantidade <= 0:
            raise ValueError("A quantidade deve ser maior que zero")
        if quantidade > produto.estoque:
            raise ValueError(
                f"estoque indisponivel para o produto {produto.nome}."
                f"Quantidade disponivel: {produto.estoque}. Solicitado: {quantidade}"
            )
        item = {
            'produto':  produto,
            "quantidade":  quantidade
        }
        self.itens.append(item)
        print(f"Adicionado ao carrinho: {produto.nome} (x{quantidade})")

    def calcular_total(self) -> float:
        total = 0.0
        for item in self.itens:
            total += item['produto'].preco * item['quantidade']
        return total

    def finalizar_compra(self) -> None:
        for item in self.itens:
            produto = item['produto']
            quantidade = item['quantidade']

        print("\nCompra finalizada com sucesso! Estoque atualizado.")
        self.itens.clear()

    def listar(self):
        print("Carrinho de Compras: ")
        if not self.itens:
            print("O carrinho está vazio.")
            return
        for item in self.itens:
            produto = item["produto"]
            quantidade = item["quantidade"]
            subtotal = produto.preco * quantidade
            print(f"- Produto: {produto.nome} | Quantidade: {quantidade} | Sub-total: R$ {subtotal:.2f}")
        print(f"Total Geral: R$ {self.calcular_total():.2f}\n")
