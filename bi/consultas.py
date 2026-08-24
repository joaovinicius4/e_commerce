from pathlib import Path
import sqlite3

import pandas as pd


CAMINHO_BANCO = Path(__file__).resolve().parent.parent / "loja.db"


def buscar_vendas() -> pd.DataFrame:
    """Retorna somente pedidos pagos, com uma linha por pedido."""
    consulta = """
        SELECT
            p.id_pedido,
            p.data_pedido,
            p.valor_total,
            p.status,
            c.nome AS cliente,
            pg.forma_pagamento
        FROM pedidos AS p
        JOIN clientes AS c
            ON c.id_cliente = p.cliente_id
        LEFT JOIN pagamentos AS pg
            ON pg.pedido_id = p.id_pedido AND pg.status = 'APROVADO'
        WHERE p.status = 'PAGO'
        ORDER BY p.data_pedido
    """

    with sqlite3.connect(CAMINHO_BANCO) as conexao:
        vendas = pd.read_sql_query(consulta, conexao)

    vendas["data_pedido"] = pd.to_datetime(vendas["data_pedido"], errors="coerce")
    return vendas.dropna(subset=["data_pedido"])


def buscar_vendas_por_produto() -> pd.DataFrame:
    """Retorna quantidade e receita dos produtos presentes em pedidos pagos."""
    consulta = """
        SELECT
            p.data_pedido,
            pr.id_produto,
            pr.nome AS produto,
            SUM(ip.quantidade) AS quantidade_vendida,
            SUM(ip.quantidade * ip.preco_unitario) AS faturamento
        FROM itens_pedido AS ip
        JOIN pedidos AS p
            ON p.id_pedido = ip.pedido_id
        JOIN produtos AS pr
            ON pr.id_produto = ip.produto_id
        WHERE p.status = 'PAGO'
        GROUP BY p.data_pedido, pr.id_produto, pr.nome
        ORDER BY quantidade_vendida DESC
    """

    with sqlite3.connect(CAMINHO_BANCO) as conexao:
        produtos = pd.read_sql_query(consulta, conexao)

    produtos["data_pedido"] = pd.to_datetime(produtos["data_pedido"], errors="coerce")
    return produtos.dropna(subset=["data_pedido"])


def buscar_estoque() -> pd.DataFrame:
    """Retorna a posição atual de estoque de todos os produtos."""
    consulta = """
        SELECT
            id_produto,
            nome AS produto,
            estoque,
            preco
        FROM produtos
        ORDER BY estoque, nome
    """

    with sqlite3.connect(CAMINHO_BANCO) as conexao:
        return pd.read_sql_query(consulta, conexao)
