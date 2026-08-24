from datetime import date

import pandas as pd
import plotly.express as px
import streamlit as st

from bi.consultas import buscar_estoque, buscar_vendas, buscar_vendas_por_produto


st.set_page_config(
    page_title="E-commerce BI",
    page_icon="📊",
    layout="wide",
)

st.markdown(
    """
    <style>
        .stApp { background: #f6f7fb; }
        [data-testid="stSidebar"] { background: #111827; }
        [data-testid="stSidebar"] * { color: #f9fafb; }
        [data-testid="stSidebar"] input {
            color: #f9fafb !important;
            -webkit-text-fill-color: #f9fafb !important;
            caret-color: #a5b4fc !important;
            background-color: #211827 !important;
        }
        [data-testid="stSidebar"] [data-baseweb="input"] {
            background-color: #211827 !important;
            border-color: #4f46e5 !important;
        }
        [data-testid="stSidebar"] [data-baseweb="base-input"] {
            background-color: #211827 !important;
        }
        [data-testid="stSidebar"] input::selection {
            color: #ffffff !important;
            background: #4f46e5 !important;
        }
        [data-testid="stSidebar"] [data-baseweb="input"] svg {
            fill: #f9fafb !important;
            color: #f9fafb !important;
        }
        [data-testid="stSidebar"] [data-testid="stNumberInput"] button svg {
            fill: #f9fafb !important;
            color: #f9fafb !important;
        }
        /* Mantém os controles escuros em todos os estados do BaseWeb. */
        [data-testid="stSidebar"] [data-testid="stDateInput"] [data-baseweb="input"],
        [data-testid="stSidebar"] [data-testid="stNumberInput"] [data-baseweb="input"],
        [data-testid="stSidebar"] [data-testid="stDateInput"] [data-baseweb="base-input"],
        [data-testid="stSidebar"] [data-testid="stNumberInput"] [data-baseweb="base-input"],
        [data-testid="stSidebar"] [data-testid="stDateInput"] input,
        [data-testid="stSidebar"] [data-testid="stNumberInput"] input {
            background: #211827 !important;
            background-color: #211827 !important;
            color: #ffffff !important;
            -webkit-text-fill-color: #ffffff !important;
            opacity: 1 !important;
        }
        [data-testid="stSidebar"] [data-testid="stDateInput"] [data-baseweb="input"],
        [data-testid="stSidebar"] [data-testid="stNumberInput"] [data-baseweb="input"] {
            border: 1px solid #4f46e5 !important;
            border-radius: 9px !important;
            box-shadow: none !important;
            overflow: hidden !important;
        }
        [data-testid="stSidebar"] [data-testid="stDateInput"] [data-baseweb="input"]:focus-within,
        [data-testid="stSidebar"] [data-testid="stNumberInput"] [data-baseweb="input"]:focus-within {
            border-color: #818cf8 !important;
            box-shadow: 0 0 0 1px #818cf8 !important;
        }
        [data-testid="stSidebar"] [data-testid="stDateInput"] input:hover,
        [data-testid="stSidebar"] [data-testid="stDateInput"] input:focus,
        [data-testid="stSidebar"] [data-testid="stDateInput"] input:active,
        [data-testid="stSidebar"] [data-testid="stNumberInput"] input:hover,
        [data-testid="stSidebar"] [data-testid="stNumberInput"] input:focus,
        [data-testid="stSidebar"] [data-testid="stNumberInput"] input:active {
            background-color: #211827 !important;
            color: #ffffff !important;
            -webkit-text-fill-color: #ffffff !important;
        }
        [data-testid="stAppViewContainer"] .main {
            color: #111827;
        }
        [data-testid="stAppViewContainer"] .main p,
        [data-testid="stAppViewContainer"] .main label,
        [data-testid="stAppViewContainer"] .main span {
            color: #374151;
        }
        [data-testid="stMetric"] {
            background: white;
            border: 1px solid #e5e7eb;
            border-radius: 14px;
            padding: 18px;
            box-shadow: 0 4px 18px rgba(17, 24, 39, 0.05);
        }
        [data-testid="stMetricLabel"] p { color: #6b7280 !important; }
        [data-testid="stMetricValue"] { color: #111827 !important; }
        h1, h2, h3 { color: #111827; }
        .subtitle { color: #6b7280; margin-top: -12px; margin-bottom: 24px; }
        .empty-state {
            padding: 42px 24px;
            text-align: center;
            background: white;
            border: 1px dashed #cbd5e1;
            border-radius: 14px;
            color: #64748b;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


def moeda(valor: float) -> str:
    formatado = f"{valor:,.2f}"
    return f"R$ {formatado.replace(',', 'X').replace('.', ',').replace('X', '.')}"


@st.cache_data(ttl=30)
def carregar_vendas() -> pd.DataFrame:
    return buscar_vendas()


@st.cache_data(ttl=30)
def carregar_vendas_por_produto() -> pd.DataFrame:
    return buscar_vendas_por_produto()


@st.cache_data(ttl=30)
def carregar_estoque() -> pd.DataFrame:
    return buscar_estoque()


with st.sidebar:
    st.title("E-commerce BI")
    st.caption("Painel gerencial")
    st.divider()
    st.markdown("**Visão geral**")
    st.caption("Vendas, pedidos e ticket médio")

st.title("Visão geral")
st.markdown(
    '<p class="subtitle">Acompanhe os principais resultados das vendas aprovadas.</p>',
    unsafe_allow_html=True,
)

try:
    vendas = carregar_vendas()
    vendas_por_produto = carregar_vendas_por_produto()
    estoque = carregar_estoque()
except Exception as erro:
    st.error("Não foi possível consultar o banco de dados.")
    st.exception(erro)
    st.stop()

if vendas.empty:
    st.markdown(
        """
        <div class="empty-state">
            <h3>Ainda não existem vendas pagas</h3>
            <p>Finalize algumas compras no e-commerce e os indicadores aparecerão aqui automaticamente.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.stop()

data_minima = vendas["data_pedido"].min().date()
data_maxima = vendas["data_pedido"].max().date()

with st.sidebar:
    st.divider()
    st.subheader("Período")
    periodo = st.date_input(
        "Selecione as datas",
        value=(data_minima, data_maxima),
        min_value=data_minima,
        max_value=data_maxima,
        label_visibility="collapsed",
    )
    st.subheader("Estoque mínimo")
    estoque_minimo = st.number_input(
        "Limite para alerta",
        min_value=1,
        max_value=1000,
        value=10,
        step=1,
        help="Produtos com estoque igual ou inferior a este valor recebem alerta.",
    )

if isinstance(periodo, (tuple, list)) and len(periodo) == 2:
    inicio, fim = periodo
else:
    inicio = fim = periodo if isinstance(periodo, date) else data_maxima

vendas_filtradas = vendas[
    vendas["data_pedido"].dt.date.between(inicio, fim)
].copy()

faturamento = vendas_filtradas["valor_total"].sum()
pedidos = vendas_filtradas["id_pedido"].nunique()
ticket_medio = faturamento / pedidos if pedidos else 0

coluna_1, coluna_2, coluna_3 = st.columns(3)
coluna_1.metric("Faturamento", moeda(faturamento))
coluna_2.metric("Pedidos pagos", f"{pedidos:,}".replace(",", "."))
coluna_3.metric("Ticket médio", moeda(ticket_medio))

st.subheader("Faturamento ao longo do tempo")

if vendas_filtradas.empty:
    st.info("Não há vendas pagas no período selecionado.")
else:
    faturamento_diario = (
        vendas_filtradas.assign(dia=vendas_filtradas["data_pedido"].dt.date)
        .groupby("dia", as_index=False)["valor_total"]
        .sum()
        .rename(columns={"valor_total": "Faturamento"})
    )

    if len(faturamento_diario) == 1:
        grafico = px.bar(
            faturamento_diario,
            x="dia",
            y="Faturamento",
            labels={"dia": "Data"},
            text_auto=True,
            color_discrete_sequence=["#4f46e5"],
        )
        grafico.update_traces(width=0.35, texttemplate="R$ %{y:,.2f}")
    else:
        grafico = px.area(
            faturamento_diario,
            x="dia",
            y="Faturamento",
            markers=True,
            labels={"dia": "Data"},
            color_discrete_sequence=["#4f46e5"],
        )
        grafico.update_traces(line={"width": 3}, fillcolor="rgba(79, 70, 229, 0.12)")
    grafico.update_layout(
        height=390,
        margin={"l": 10, "r": 10, "t": 20, "b": 10},
        paper_bgcolor="white",
        plot_bgcolor="white",
        font={"color": "#374151"},
        hovermode="x unified",
        xaxis={"showgrid": False},
        yaxis={"gridcolor": "#eef0f4", "tickprefix": "R$ "},
    )
    st.plotly_chart(grafico, use_container_width=True)

st.subheader("Produtos mais vendidos")

produtos_filtrados = vendas_por_produto[
    vendas_por_produto["data_pedido"].dt.date.between(inicio, fim)
].copy()

if produtos_filtrados.empty:
    st.info("Não há produtos vendidos no período selecionado.")
else:
    ranking_produtos = (
        produtos_filtrados.groupby("produto", as_index=False)
        .agg(
            quantidade_vendida=("quantidade_vendida", "sum"),
            faturamento=("faturamento", "sum"),
        )
        .sort_values(["quantidade_vendida", "faturamento"], ascending=False)
        .head(5)
    )

    coluna_quantidade, coluna_receita = st.columns(2)

    grafico_quantidade = px.bar(
        ranking_produtos.sort_values("quantidade_vendida"),
        x="quantidade_vendida",
        y="produto",
        orientation="h",
        text="quantidade_vendida",
        labels={
            "produto": "",
            "quantidade_vendida": "Unidades vendidas",
            "faturamento": "Faturamento",
        },
        hover_data={"faturamento": ":.2f"},
        color_discrete_sequence=["#4f46e5"],
        title="Por quantidade",
    )
    grafico_quantidade.update_traces(textposition="outside", cliponaxis=False)

    grafico_receita = px.bar(
        ranking_produtos.sort_values("faturamento"),
        x="faturamento",
        y="produto",
        orientation="h",
        text="faturamento",
        labels={
            "produto": "",
            "faturamento": "Receita gerada",
            "quantidade_vendida": "Unidades vendidas",
        },
        hover_data={"quantidade_vendida": True},
        color_discrete_sequence=["#0891b2"],
        title="Por faturamento",
    )
    grafico_receita.update_traces(
        texttemplate="R$ %{x:,.2f}",
        textposition="outside",
        cliponaxis=False,
    )

    for grafico_produto in (grafico_quantidade, grafico_receita):
        grafico_produto.update_layout(
            height=360,
            margin={"l": 10, "r": 50, "t": 55, "b": 10},
            paper_bgcolor="white",
            plot_bgcolor="white",
            font={"color": "#374151"},
            showlegend=False,
            xaxis={"showgrid": True, "gridcolor": "#eef0f4"},
            yaxis={"showgrid": False},
        )

    coluna_quantidade.plotly_chart(grafico_quantidade, use_container_width=True)
    coluna_receita.plotly_chart(grafico_receita, use_container_width=True)

st.subheader("Controle de estoque")

vendas_resumidas = (
    produtos_filtrados.groupby("id_produto", as_index=False)["quantidade_vendida"]
    .sum()
    if not produtos_filtrados.empty
    else pd.DataFrame(columns=["id_produto", "quantidade_vendida"])
)

controle_estoque = estoque.merge(vendas_resumidas, on="id_produto", how="left")
controle_estoque["quantidade_vendida"] = (
    controle_estoque["quantidade_vendida"].fillna(0).astype(int)
)
controle_estoque["sugestao_reposicao"] = (
    (estoque_minimo * 2 - controle_estoque["estoque"]).clip(lower=0).astype(int)
)


def classificar_estoque(linha: pd.Series) -> str:
    if linha["estoque"] <= estoque_minimo and linha["quantidade_vendida"] > 0:
        return "🔴 Repor com prioridade"
    if linha["estoque"] <= estoque_minimo:
        return "🟠 Estoque baixo"
    return "🟢 Estoque adequado"


controle_estoque["situacao"] = controle_estoque.apply(classificar_estoque, axis=1)
controle_estoque = controle_estoque.sort_values(
    ["sugestao_reposicao", "quantidade_vendida"], ascending=[False, False]
)

produtos_em_alerta = int((controle_estoque["estoque"] <= estoque_minimo).sum())
unidades_para_repor = int(controle_estoque["sugestao_reposicao"].sum())
produto_mais_urgente = (
    controle_estoque.iloc[0]["produto"] if unidades_para_repor else "Nenhum"
)

estoque_coluna_1, estoque_coluna_2, estoque_coluna_3 = st.columns(3)
estoque_coluna_1.metric("Produtos em alerta", produtos_em_alerta)
estoque_coluna_2.metric("Reposição sugerida", f"{unidades_para_repor} un.")
estoque_coluna_3.metric("Maior prioridade", produto_mais_urgente)

tabela_estoque = controle_estoque.rename(
    columns={
        "produto": "Produto",
        "estoque": "Estoque atual",
        "quantidade_vendida": "Vendas no período",
        "sugestao_reposicao": "Reposição sugerida",
        "situacao": "Situação",
    }
)[
    [
        "Produto",
        "Estoque atual",
        "Vendas no período",
        "Reposição sugerida",
        "Situação",
    ]
]

st.dataframe(
    tabela_estoque,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Produto": st.column_config.TextColumn(width="large"),
        "Estoque atual": st.column_config.NumberColumn(format="%d un."),
        "Vendas no período": st.column_config.NumberColumn(format="%d un."),
        "Reposição sugerida": st.column_config.NumberColumn(format="%d un."),
        "Situação": st.column_config.TextColumn(width="medium"),
    },
)

st.caption(
    "A reposição sugerida completa o estoque até duas vezes o limite mínimo configurado."
)

st.caption("Os indicadores consideram somente pedidos com status PAGO.")
