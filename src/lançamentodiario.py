import pandas as pd
from dataframe import Dataframesvenda, Dataframescompra, DataframesEstoque
from compras import Lançarcomprasnoestoque
from vendas import Lançarvendasnoestoque


def lancaropdia(dados):
    novoprod = []
    contasapagar = []
    vendad = []
    vendasareceber = []
    caixa = dados["Caixa"]
    estoque = dados["Estoque"]
    ComprasTotal = dados["Compras"]
    VendasTotal = dados["Vendas"]
    nomearq = dados["nomearq"]
    valoreb = dados["A Receber"]
    valorpag = dados["A Pagar"]
    clientes = dados["Clientes"]

    print('Verificando produtos que estão no estoque..')
    for _,linha in caixa.iterrows():
        produto = linha["Nome do produto"]
        Tamanho = linha["Tamanho"]
        qnt = linha["Quantidade"]
        valoruni = linha["Valor unitario compra"]
        operacao = linha["Operação"]
        data = linha["Data"]
        sexo = linha["Sexo"]
        Participante = linha["Participante"]  

        ##  cria dataframes para registrar as compras, vendas, contas a pagar e contas a receber
        NovaVenda = Dataframesvenda(Participante, produto, Tamanho, sexo, qnt, valoruni, data)
        NovaCompra = Dataframescompra(produto, Tamanho, sexo, qnt, valoruni, data)
        NovalinhaEstoque = DataframesEstoque(produto, Tamanho, qnt, valoruni) 

        if operacao == "Compra":
            ComprasTotal, estoque, valorpag = Lançarcomprasnoestoque(linha, estoque, ComprasTotal, NovaCompra, NovalinhaEstoque, valorpag, novoprod, contasapagar)
        elif operacao == "Venda":
            VendasTotal, estoque, valoreb, clientes = Lançarvendasnoestoque(VendasTotal, linha, estoque, valoreb, clientes , NovaVenda, vendad, vendasareceber)
        else:
               print(f"Foi encontrado uma operação invalida, verifique as operações lançadas no caixa! Operação: {operacao}!")


    dados_atualizados = {
        "Caixa": caixa,
        "Compras": ComprasTotal,
        "Vendas": VendasTotal,
        "Estoque": estoque,
        "A Receber": valoreb,
        "A Pagar": valorpag,
        "Clientes": clientes,}
    

# Relatorio de compras 
    if novoprod:
      novoprod = pd.concat(novoprod, ignore_index=True)
    else:
     novoprod = pd.DataFrame()

    if not novoprod.empty:
        print("Os novos produtos cadastrados foram:")
    for _, prod in novoprod.iterrows():
        nome = prod["Nome do produto"]
        tamanho = prod["Tamanho"]
        print(f"{nome} - {tamanho}")
    else:
        print("Nenhum novo produto foi cadastrado no estoque.")

# Relatorio de vendas
    if vendad:
        vendad = pd.concat(vendad, ignore_index=True)
    else:
        vendad = pd.DataFrame()

    if not vendad.empty:
        print("As vendas realizadas foram:")
    for _, vend in vendad.iterrows():
        nome = vend["Nome do produto"]
        tamanho = vend["Tamanho"]
        data = vend["Data"]
        print(f"{nome} - {tamanho} - Data: {data}")
    else:
        print("Nenhuma venda foi realizada hoje.")

    return dados_atualizados, nomearq
