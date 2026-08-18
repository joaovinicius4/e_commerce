from database import engine, Base, session
from entities.produto import Produto
from entities.cliente import Cliente
from entities.pedido import Pedido
from services.carrinho import Carrinho

Base.metadata.create_all(bind=engine)

def main():
    while True:
        print("\nSISTEMA DE E-COMMERCE")
        print("1. Iniciar Compras (Identificar/Cadastrar Cliente)")
        print("2. Listar Produtos Disponíveis")
        print("0. Sair")
        
        opcao = input("\nEscolha uma opção: ")

        if opcao == "1":
            print("\n- IDENTIFICAÇÃO DO CLIENTE -")
            ja_cadastrado = input("Você já possui cadastro? (s/n): ").strip().lower()

            cliente_atual = None

            if ja_cadastrado == 's':
                cpf_busca = input("Digite o seu CPF: ").strip()
                cliente_atual = session.query(Cliente).filter_by(cpf=cpf_busca).first()
                
                if not cliente_atual:
                    print("\nCliente não encontrado com esse CPF!")
                    criar_agora = input("Deseja fazer o cadastro agora? (s/n): ").strip().lower()
                    if criar_agora != 's':
                        print("Cadastro cancelado!")
                        continue
                    ja_cadastrado = 'n'

            if ja_cadastrado == 'n':
                print("\n--- NOVO CADASTRO DE CLIENTE ---")
                cpf = input("CPF: ").strip()

                cliente_existente = session.query(Cliente).filter_by(cpf=cpf).first()

                if cliente_existente:
                    print(f"\nAtenção: Já existe um cliente cadastrado com o CPF {cpf}!")
                    print(f"Nome: {cliente_existente.nome} (ID: {cliente_existente.id_cliente})")
                    
                    usario_existente = input("Deseja prosseguir com este cadastro? (s/n): ").strip().lower()
                    if usario_existente == 's':
                        cliente_atual = cliente_existente
                    else:
                        print("Cadastro cancelado.")
                        continue
                else:
                    nome = input("Nome completo: ")
                    email = input("E-mail: ")
                    endereco = input("Endereço: ")
                    try:
                        cliente_atual = Cliente(nome=nome, cpf=cpf, email=email, endereco=endereco)
                        session.add(cliente_atual)
                        session.commit()
                        print(f"Cadastro realizado com sucesso! Bem-vindo(a), {cliente_atual.nome} (ID: {cliente_atual.id_cliente})")
                    except Exception as e:
                        session.rollback()
                        print(f"Erro ao cadastrar cliente: {e}")
                        continue
            if not cliente_atual:
                continue

            carrinho_atual = Carrinho()
            print(f"\nCarrinho aberto para: {cliente_atual.nome}")

            while True: 
                print("\nSub-menu de compras: ")
                print("1. Ver Produtos Disponíveis")
                print("2. Adicionar Produto ao Carrinho")
                print("3. Ver Carrinho")
                print("4. Finalizar Compra (Gerar Pedido)")
                print("0. Sair do Carrinho (Voltar ao Menu Principal)")

                sub_opcao = input("Escolha uma opção: ")

                if sub_opcao == '1':
                    print("\n-PRODUTOS DISPONÍVEIS-")
                    produtos = session.query(Produto).all()
                    for p in produtos:
                        print(f"ID: {p.id_produto} | {p.nome} | R$ {p.preco:.2f} | Estoque: {p.estoque}")
                elif sub_opcao == '2':
                    id_prod = input("Qual id do produto deseja inserir: ")
                    qtd = int(input("Quantidade: "))
                    prod = session.get(Produto, id_prod)
                    if prod:
                        carrinho_atual.adicionar_produto(prod, qtd)
                    else:
                        print("Produto não encontrado!")
                elif sub_opcao == '3':
                    print (f"Carrinho no momento: {carrinho_atual.listar()}")
                elif sub_opcao == "4":
                    if not carrinho_atual.itens:
                        print("Carrinho esta vazio!")
                        continue
                    else:
                        try:
                            novo_pedido = Pedido(carrinho_atual, cliente_atual)
                            session.add(novo_pedido)
                            novo_pedido.confirmar_pedido()
                            session.commit()
                            print(f"Pedido #{novo_pedido.id_pedido} gerado e salvo com sucesso!")
                            break
                        except Exception as e:
                            session.rollback()
                            print(f"Erro ao finalizar pedido: {e}")
                elif sub_opcao == '0':
                    print("Saindo do carrinho")
                    break
       # elif opcao == '2':
                

if __name__ == "__main__":
    main()
                    