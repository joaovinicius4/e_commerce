from models.pedido import Pedido
from services.servico_pagamento import ServicoPagamento

class PedidoService:
    def __init__(self, session):
        self.session = session
        self.servico_pagamento = ServicoPagamento(session)

    def finalizar_pedido(self, cliente, carrinho, forma_pagamento, dados_pagamento=None):
        try:
            print("\n--- Iniciando processo de finalização do pedido ---")
            if not carrinho or not carrinho.itens:
                raise ValueError("O carrinho está vazio. Não é possível finalizar o pedido.")

            novo_pedido = Pedido(
                cliente=cliente,
                valor_total=carrinho.calcular_total(),
                itens_carrinho=carrinho.itens
            )
            self.session.add(novo_pedido)
            
            # O SQLAlchemy precisa "escrever" temporariamente no banco para gerar o id_pedido 
            # caso os itens precisem dele, mas mantemos tudo preso na transação.
            self.session.flush() 

            novo_pedido.validar_e_baixar_estoque()

            pagamento_aprovado = self.servico_pagamento.processar_pagamento(
                pedido=novo_pedido,
                forma_pagamento=forma_pagamento,
                dados_pagamento=dados_pagamento
            )

            if not pagamento_aprovado:
                raise Exception("O pagamento não foi aprovado pela instituição financeira.")
            
            self.session.commit()
            print(f" Pedido #{novo_pedido.id_pedido} finalizado e salvo com sucesso!")
            
            return novo_pedido
        except Exception as e:
            self.session.rollback()
            print(f"Erro crítico ao finalizar o pedido. Transação cancelada (Rollback executado).")
            print(f"Motivo: {e}")
            raise e