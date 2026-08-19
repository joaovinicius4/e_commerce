from models.pagamento import Pagamento

class ServicoPagamento:
    def __init__(self, session):
        self.session = session
    
    def processar_pagamento(self, pedido, forma_pagamento, dados_pagamento=None):
        print(f"Processando pagamento do pedido {pedido.id_pedido}...")

        forma = forma_pagamento.lower()
        
        if forma == "pix":
            return self._registrar_e_aprovar(pedido, forma, "PIX_CONFIRMADO")
            
        elif forma == "cartao":
            if not dados_pagamento or len(dados_pagamento.get("token_cartao", "")) < 5:
                self._registrar_e_recusar(pedido, forma, "Dados ou token de cartão inválidos.")
                return False
    
            aprovado = True 
            if aprovado:
                return self._registrar_e_aprovar(pedido, forma, "APROVADO_CARTAO")
            else:
                self._registrar_e_recusar(pedido, forma, "Transação recusada pelo banco emissor.")
                return False
        else:
            self._registrar_e_recusar(pedido, forma, "Forma de pagamento não suportada.")
            return False

    def _registrar_e_aprovar(self, pedido, forma_pagamento, codigo_transacao):
        novo_pagamento = Pagamento(
            pedido_id=pedido.id_pedido,
            forma_pagamento=forma_pagamento,
            status="APROVADO",
            valor=pedido.valor_total,
            codigo_transacao=codigo_transacao
        )
        self.session.add(novo_pagamento)

        pedido.status = "PAGO"
        print(f"Pagamento aprovado para o pedido #{pedido.id_pedido} (Transação: {codigo_transacao}).")
        return True

    def _registrar_e_recusar(self, pedido, forma_pagamento, motivo):
        novo_pagamento = Pagamento(
            pedido_id=pedido.id_pedido,
            forma_pagamento=forma_pagamento,
            status="RECUSADO",
            valor=pedido.valor_total,
            codigo_transacao=None
        )
        self.session.add(novo_pagamento)
        pedido.status = "PAGAMENTO_RECUSADO"
        print(f"Pagamento recusado: {motivo}")
        return False