import pandas as pd
from dataframe import Dataframescompra, DataframesEstoque

def dataframes(produto, Tamanho, Sexo, Quantidade, ValorU, DataC):
    NovaCompra = Dataframescompra(produto, Tamanho, Sexo, Quantidade, ValorU, DataC)
    NovalinhaEstoque = DataframesEstoque(produto, Tamanho, Quantidade, ValorU)
    return NovaCompra, NovalinhaEstoque

def Lançarcomprasnoestoque(Linhacaixa, estoque ,CompTotal, dado, NovaCompra, NovalinhaEstoque):
    novoprod = []
    contasapagar = []
    nomearq = dado["nomearq"]
    valorpag = dado["A Pagar"]
    estoque = dado["Estoque"]
    produto = Linhacaixa["Nome do produto"]
    Tamanho = Linhacaixa["Tamanho"]
    Sexo = Linhacaixa["Sexo"]
    Quantidade = Linhacaixa["Quantidade"]
    ValorU = Linhacaixa["Valor unitario compra"]
    DataC = Linhacaixa["Data"]
    Partic = Linhacaixa["Participante"]
    Pagamento = Linhacaixa["Forma Pag"]
    Parcelas = Linhacaixa["Parcelas"]
    condicao = ((estoque["Nome do produto"] == produto) &  (estoque["Tamanho"] == Tamanho))
    if condicao.any():
         print(f"Condição True - produto: {produto} Tamanho: {Tamanho} ")
         qntattest = estoque.loc[condicao, "Quantidade"].iloc[0] + Quantidade
         estoque.loc[condicao, "Quantidade"] = qntattest
    else:
         print(f"Condição False - produto: {produto} Tamanho: {Tamanho} ")
         estoque = pd.concat([estoque, NovalinhaEstoque], ignore_index=True)
         novoprod.append(NovalinhaEstoque)

    CompTotal = pd.concat([CompTotal, NovaCompra], ignore_index=True)
    if Pagamento == "Parcelado":
                print("Identificado parcelado")
                valor_total = ValorU * Quantidade
                valor_parcela = valor_total / Parcelas
                for i in range(Parcelas):
                    totalatualizado = valor_total - (valor_parcela * i)
                    vencimento = DataC + pd.DateOffset(months=i+1)
                    nova_parcela_compra = pd.DataFrame([{ "Participante": Partic,
                                                      "Nome do produto": produto,
                                                      "Parcela": i+1,
                                                      "Valor parcela": valor_parcela,
                                                      "Valor total": valor_total,
                                                      "Valor total pendente": totalatualizado,
                                                      "Data vencimento": vencimento,}])
                    if valorpag.empty:
                        valorpag = nova_parcela_compra
                    else:
                        valorpag = pd.concat([valorpag, nova_parcela_compra], ignore_index=True)
                contasapagar.append(nova_parcela_compra)
    with pd.ExcelWriter(nomearq, mode="a", if_sheet_exists='replace', engine="openpyxl") as writer:
        CompTotal.to_excel(writer, sheet_name="Compras", index=False)
        valorpag.to_excel(writer, sheet_name="A Pagar", index=False)
        estoque.to_excel(writer, sheet_name="Estoque", index=False)
    dado["Estoque"] = estoque
    dado["Compras"] = CompTotal
    dado["A Pagar"] = valorpag