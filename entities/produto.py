class Produto:
    def __init__(self, id_produto: int, nome: str, preco: float, estoque: int):
        
        self.id_produto = id_produto
        self.nome = nome
        self.preco = preco
        self.estoque = estoque

    def __str__(self) -> str:
        return f"Produto: {self.nome}, Codigo: {self.id_produto}, Preço: {self.preco}, Quantidade em estoque: {self.estoque}"

    def adicionar_estoque(self, quantidade: int) -> None:
        if quantidade > 0:
            self.estoque += quantidade

    def remover_estoque(self, quantidade: int) -> None:
        if quantidade <= 0:
            raise ValueError("A quantidade a ser removida deve ser maior que zero.")
        
        if quantidade > self.estoque:
            raise ValueError(f"Estoque insuficiente. Disponível: {self.estoque}, solicitado: {quantidade}")
            
        self.estoque -= quantidade
        
