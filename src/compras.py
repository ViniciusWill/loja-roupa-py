import pandas as pd

def Lançarcomprasnoestoque(Linhacaixa, estoque ,CompTotal, Ncompra, NLEstoque, valorpag, novoprod, contasapagar):
    produto = Linhacaixa["Nome do produto"]
    Tamanho = Linhacaixa["Tamanho"]
    Quantidade = Linhacaixa["Quantidade"]
    ValorU = Linhacaixa["Valor unitario compra"]
    DataC = Linhacaixa["Data"]
    Partic = Linhacaixa["Participante"]
    Pagamento = Linhacaixa["Forma Pag"]
    Parcelas = Linhacaixa["Parcelas"]

    condicao = ((estoque["Nome do produto"] == produto) &  (estoque["Tamanho"] == Tamanho))
   
    if condicao.any():
         qntattest = estoque.loc[condicao, "Quantidade"].iloc[0] + Quantidade
         estoque.loc[condicao, "Quantidade"] = qntattest
    else:
         estoque = pd.concat([estoque, NLEstoque], ignore_index=True)
         novoprod.append(NLEstoque)

    CompTotal = pd.concat([CompTotal, Ncompra], ignore_index=True)
    if Pagamento == "Parcelado":
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
    

    return CompTotal, estoque, valorpag