import pandas as pd

dt = pd.read_csv("data/vendas_tratadas.csv")

def somaquantidadevendida ():
    vendasPorProduto = dt.groupby("Produto")["Quantidade"].sum().reset_index()
    return vendasPorProduto

def calcular_faturamento (dt, data='data_venda', valorTotal='Total_Venda', inicio=None, fim=None, frequencia='ME'):
    df_trab = dt.copy()

## conversão de campo data para Datetime
    df_trab[data] = pd.to_datetime(df_trab[data])

    if inicio:
        df_trab = df_trab[df_trab[data] >= pd.to_datetime(inicio)]
    if fim:
        df_trab = df_trab[df_trab[data] <= pd.to_datetime(fim)]

    resultado = (
        df_trab.set_index(data)
        .resample(frequencia)[valorTotal]
        .sum()
        .reset_index()
    )

    return resultado

def vendedorDeSucesso (dt, vendedor='Vendedor', data='data_venda', valorTotal='Total_Venda', frequencia='ME'):

    df_trab = dt.copy()

    df_trab[data] = pd.to_datetime(df_trab[data])

    vendas = (
        df_trab
        .groupby([
            df_trab[data].dt.to_period(frequencia),
            vendedor])[valorTotal]
        .sum()
        .reset_index()

    )

    vendedor_sucesso = (
        vendas
        .loc[vendas.groupby(data)[valorTotal].idxmax()]
        .reset_index(drop=True)
    )

    return vendedor_sucesso


def produtoSucesso (dt, data='data_venda',produto='Produto', quantidade='Quantidade', valorTotal='Total_Venda', frequencia='ME'):
    df_trab = dt.copy()
    df_trab[data] = pd.to_datetime(df_trab[data])

    produtosvendidos = df_trab.groupby(produto)[[quantidade, valorTotal]].sum().sort_values(by=quantidade, ascending = False).head(10)


    return produtosvendidos


df_teste = dt.copy()
df_teste = produtoSucesso(dt)

print(df_teste)


