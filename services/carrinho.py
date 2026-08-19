from models.produto import Produto
class Carrinho:
    def __init__(self):
        self.itens = []

    def adicionar_produto(self, produto: Produto, quantidade: int) -> None:
        if quantidade <= 0:
            raise ValueError("A quantidade deve ser maior que zero")
            
        for item in self.itens:
            if item['produto'] == produto:
                nova_qtd = item['quantidade'] + quantidade
                if nova_qtd > produto.estoque:
                    raise ValueError(
                        f"Estoque indisponível para o produto {produto.nome}. "
                        f"Disponível: {produto.estoque}. Total solicitado: {nova_qtd}"
                    )
                item['quantidade'] = nova_qtd
                print(f"Quantidade atualizada no carrinho: {produto.nome} (total: x{nova_qtd})")
                return

        if quantidade > produto.estoque:
            raise ValueError(
                f"Estoque indisponível para o produto {produto.nome}."
                f"Quantidade disponivel: {produto.estoque}. Solicitado: {quantidade}"
            )
        item = {
            'produto': produto,
            'quantidade': quantidade
        }
        self.itens.append(item)
        print(f"Adicionado ao carrinho: {produto.nome} (x{quantidade})")
        
    def calcular_total(self) -> float:
        total = 0.0
        for item in self.itens:
            total += item['produto'].preco * item['quantidade']
        return total

    def finalizar_compra(self) -> None:
        self.itens.clear()
        print("\nCarrinho esvaziado com sucesso.")

    def listar(self):
        if not self.itens:
            print("O carrinho está vazio.")
            return
        for item in self.itens:
            produto = item["produto"]
            quantidade = item["quantidade"]
            subtotal = produto.preco * quantidade
            print(f"- Produto: {produto.nome} | Quantidade: {quantidade} | Sub-total: R$ {subtotal:.2f}")
        print(f"Total Geral: R$ {self.calcular_total():.2f}\n")
