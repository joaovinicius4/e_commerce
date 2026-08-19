import random
from models.pedido import Pedido
from models.cliente import Cliente

class ServicoPagamento:
    def __init__(self, session):
        self.session = session

    def metodo_pagamento(self, pedido, forma_pagamento, dados_cartao=None):
        print(f"processando pagamento para o cliente: {pedido.cliente_id.nome}")

        if forma_pagamento.lower() == 'pix':
            return self._aprovar_pagamento(pedido, "PIX_CONFIRMADO")
        elif forma_pagamento.lower() == 'cartão':
            if not dados_cartao or len(dados_cartao.get("numero", "") < 13):
                 return self._recusar_pagamento(pedido, "Dados de cartão inválidos.")
            sucesso = random.choice([True, True, True, False]) # 75% de chance de aprovar
            if sucesso:
                return self._aprovar_pagamento(pedido, "APROVADO_CARTAO")
            else:
                return self._recusar_pagamento(pedido, "Transação recusada pelo banco emissor.")
        else:
            return self._recusar_pagamento(pedido, "Metodo não suportado.")

        


        