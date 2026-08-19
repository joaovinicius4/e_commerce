import random
from models.pagamento import Pagamento


class ServicoPagamento:
    def __init__(self, session):
        self.session = session

    def metodo_pagamento(self, pedido, forma_pagamento, dados_cartao=None):
        print(f"Processando pagamento para o cliente: {pedido.cliente.nome}")
        pagamento = Pagamento(
            pedido=pedido,
            forma_pagamento=forma_pagamento,
            valor=pedido.valor_total
        )
        self.session.add(pagamento)
        self.session.commit()

        if forma_pagamento.lower() == "pix":
            return self._aprovar_pagamento(pagamento,"PIX_CONFIRMADO")
        elif forma_pagamento.lower() == "cartão":
            if not dados_cartao or len(dados_cartao.get("numero", "")) < 13:
                return self._recusar_pagamento(pagamento, "Dados de cartão inválidos.")
            sucesso = random.choice([True, True, True, False])
            if sucesso:
                return self._aprovar_pagamento(pagamento, "CARTAO_APROVADO")
            else:
                return self._recusar_pagamento(pagamento, "Transação recusada pelo banco emissor.")
        else:
            return self._recusar_pagamento(pagamento, "Método não suportado.")

    def _aprovar_pagamento(self, pagamento, codigo_transacao):
        pagamento.status = "PAGO"
        pagamento.codigo_transacao = codigo_transacao
        self.session.commit()
        print(
            f"Pagamento APROVADO! "
            f"Pedido #{pagamento.pedido.id_pedido} está PAGO."
        )
        return True

    def _recusar_pagamento(self, pagamento, motivo):
        pagamento.status = "PAGAMENTO_RECUSADO"
        self.session.commit()
        print(f"Pagamento RECUSADO: {motivo}")
        return False