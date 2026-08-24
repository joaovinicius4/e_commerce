"""Popula o banco com dados históricos fictícios para demonstração do BI."""

from datetime import datetime, timedelta
from pathlib import Path
import random
import sqlite3


CAMINHO_BANCO = Path(__file__).resolve().parent / "loja.db"
SEMENTE = 20260824

CLIENTES_DEMO = [
    ("90000000001", "Mariana Costa", "mariana.costa@demo-bi.local", "Rua das Flores, 120"),
    ("90000000002", "Lucas Almeida", "lucas.almeida@demo-bi.local", "Av. Central, 455"),
    ("90000000003", "Fernanda Lima", "fernanda.lima@demo-bi.local", "Rua do Comércio, 82"),
    ("90000000004", "Rafael Martins", "rafael.martins@demo-bi.local", "Av. Brasil, 910"),
    ("90000000005", "Camila Ribeiro", "camila.ribeiro@demo-bi.local", "Rua Primavera, 33"),
    ("90000000006", "Bruno Carvalho", "bruno.carvalho@demo-bi.local", "Rua das Acácias, 210"),
    ("90000000007", "Juliana Rocha", "juliana.rocha@demo-bi.local", "Av. Paulista, 1500"),
    ("90000000008", "Gabriel Souza", "gabriel.souza@demo-bi.local", "Rua da Paz, 71"),
    ("90000000009", "Larissa Mendes", "larissa.mendes@demo-bi.local", "Rua Horizonte, 640"),
    ("90000000010", "Diego Oliveira", "diego.oliveira@demo-bi.local", "Av. das Nações, 305"),
]


def popular() -> None:
    aleatorio = random.Random(SEMENTE)

    with sqlite3.connect(CAMINHO_BANCO) as conexao:
        cursor = conexao.cursor()

        ja_populado = cursor.execute(
            "SELECT COUNT(*) FROM pagamentos WHERE codigo_transacao LIKE 'DEMO-BI-%'"
        ).fetchone()[0]
        if ja_populado:
            print("Os dados DEMO-BI já existem. Nenhum registro foi duplicado.")
            return

        produtos = cursor.execute(
            "SELECT id_produto, preco FROM produtos ORDER BY id_produto"
        ).fetchall()
        if not produtos:
            raise RuntimeError("Cadastre produtos antes de gerar os dados de demonstração.")

        for cliente in CLIENTES_DEMO:
            cursor.execute(
                """
                INSERT OR IGNORE INTO clientes (cpf, nome, email, endereco)
                VALUES (?, ?, ?, ?)
                """,
                cliente,
            )

        clientes_ids = [
            linha[0]
            for linha in cursor.execute(
                "SELECT id_cliente FROM clientes WHERE email LIKE '%@demo-bi.local'"
            ).fetchall()
        ]

        agora = datetime.now()
        pedidos_criados = 0
        pedidos_pagos = 0

        for numero in range(1, 41):
            dias_atras = 1 + ((numero * 37) % 45)
            data_pedido = agora - timedelta(
                days=dias_atras,
                hours=aleatorio.randint(0, 18),
                minutes=aleatorio.randint(0, 59),
            )
            cliente_id = aleatorio.choice(clientes_ids)
            itens_escolhidos = aleatorio.sample(
                produtos, k=aleatorio.randint(1, min(3, len(produtos)))
            )

            itens = []
            valor_total = 0.0
            for produto_id, preco in itens_escolhidos:
                quantidade = aleatorio.randint(1, 3)
                itens.append((produto_id, quantidade, preco))
                valor_total += quantidade * preco

            # A maioria representa vendas concluídas; alguns registros exercitam os status.
            if numero in (13, 31):
                status_pedido = "CANCELADO"
                status_pagamento = "CANCELADO"
            elif numero in (7, 26):
                status_pedido = "PAGAMENTO_RECUSADO"
                status_pagamento = "RECUSADO"
            else:
                status_pedido = "PAGO"
                status_pagamento = "APROVADO"
                pedidos_pagos += 1

            cursor.execute(
                """
                INSERT INTO pedidos (valor_total, data_pedido, status, cliente_id)
                VALUES (?, ?, ?, ?)
                """,
                (
                    round(valor_total, 2),
                    data_pedido.isoformat(sep=" "),
                    status_pedido,
                    cliente_id,
                ),
            )
            pedido_id = cursor.lastrowid

            cursor.executemany(
                """
                INSERT INTO itens_pedido
                    (pedido_id, produto_id, quantidade, preco_unitario)
                VALUES (?, ?, ?, ?)
                """,
                [
                    (pedido_id, produto_id, quantidade, preco)
                    for produto_id, quantidade, preco in itens
                ],
            )

            forma_pagamento = aleatorio.choice(["pix", "pix", "cartao"])
            cursor.execute(
                """
                INSERT INTO pagamentos
                    (pedido_id, forma_pagamento, status, valor,
                     codigo_transacao, data_pagamento)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    pedido_id,
                    forma_pagamento,
                    status_pagamento,
                    round(valor_total, 2),
                    f"DEMO-BI-{numero:03d}",
                    (data_pedido + timedelta(minutes=aleatorio.randint(1, 20))).isoformat(
                        sep=" "
                    ),
                ),
            )
            pedidos_criados += 1

        conexao.commit()

    print(f"Clientes de demonstração disponíveis: {len(CLIENTES_DEMO)}")
    print(f"Pedidos criados: {pedidos_criados} ({pedidos_pagos} pagos)")
    print("O estoque atual não foi alterado, pois as vendas representam histórico.")


if __name__ == "__main__":
    popular()
