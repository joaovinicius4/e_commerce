from entities.produto import Produto
from entities.cliente import Cliente
from entities.carrinho import Carrinho
from entities.pedido import Pedido

def main():
    print("SISTEMA DE E-COMMERCE INTERATIVO\n")

    print("--- 1. Cadastro do Produto ---")
    nome_prod = input("Nome do produto: ")
    preco_prod = float(input("Preço do produto (ex: 150.50): "))
    estoque_prod = int(input("Quantidade inicial em estoque: "))
    

    produto = Produto(1, nome_prod, preco_prod, estoque_prod)
    print(f"Produto '{produto.nome}' cadastrado com sucesso!\n")

    print("2. Cadastro do Cliente")
    nome_cli = input("Seu nome: ")
    email_cli = input("Seu e-mail: ")
    
    cliente = Cliente(1, nome_cli, email_cli)
    print(f"Bem-vindo(a), {cliente.nome}!\n")
    
    carrinho = Carrinho()

    try:
        print("--- 3. Compras ---")
        print(f"Produto disponível: {produto.nome} | Preço: R$ {produto.preco:.2f} | Estoque: {produto.estoque}")
        
        qtd_desejada = int(input(f"Quantas unidades de '{produto.nome}' você deseja comprar? "))
        
        carrinho.adicionar_produto(produto, qtd_desejada)
        
        print("\n--- RESUMO DO CARRINHO ---")
        carrinho.listar()

        confirmar = input("Deseja confirmar e fechar o pedido? (s/n): ").strip().lower()
        
        if confirmar == 's':
            pedido = Pedido(carrinho=carrinho, id_pedido=101, cliente=cliente)
            print("\n--- DADOS DO PEDIDO ---")
            print(pedido)

            pedido.confirmar_pedido()

            carrinho.finalizar_compra()

            print(f"\nEstoque restante de '{produto.nome}': {produto.estoque} unidades.")
        else:
            print("\nCompra cancelada pelo usuário.")

    except ValueError as e:
        print(f"\n[ERRO]: {e}")

if __name__ == "__main__":
    main()