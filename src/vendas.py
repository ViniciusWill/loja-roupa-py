import pandas as pd 

def Lançarvendasnoestoque(VendasT, Linhacaixa, estoque, ValorReceb, clientes , NVenda, vendad, vendasareceber): 
    produto = Linhacaixa["Nome do produto"]
    Tamanho = Linhacaixa["Tamanho"]
    Quantidade = Linhacaixa["Quantidade"]
    DataV = Linhacaixa["Data"]
    Pagamento = Linhacaixa["Forma Pag"]
    ValorV = Linhacaixa["Valor unitario venda"]
    Parcelas = Linhacaixa["Parcelas"]
    Participante = Linhacaixa["Participante"]

    condicao = ((estoque["Nome do produto"] == produto) &  (estoque["Tamanho"] == Tamanho))

    if condicao.any():
        qntattest = estoque.loc[condicao, "Quantidade"].iloc[0] - Quantidade
            ## verifica se há unidades disponiveis para venda, se sim, atualiza o estoque e registra a venda, se não, exibe mensagem de erro
        if Quantidade >= 0:
            estoque.loc[condicao, "Quantidade"] = qntattest
            vendad.append(NVenda)  
            VendasT = pd.concat([VendasT,NVenda], ignore_index=True)  
        elif Quantidade < 0:
         print('Não há unidades do produto disponiveis para venda!')
           
        if Pagamento == "Parcelado":    
                        valor_total = ValorV * Quantidade
                        valor_parcela = valor_total / Parcelas
                        for i in range(Parcelas):
                            totalatualizado = valor_total - (valor_parcela * i)
                            vencimento = DataV + pd.DateOffset(months=i+1)
                            nova_parcela_venda = pd.DataFrame([{ "Cliente": Participante,
                                                          "Nome do produto": produto,
                                                          "Parcela": i+1,
                                                          "Valor parcela": valor_parcela,
                                                          "Valor total": valor_total, 
                                                          "Valor total pendente": totalatualizado,
                                                          "Data vencimento": vencimento,}])
                            if ValorReceb.empty:
                                ValorReceb = nova_parcela_venda
                            else:
                                ValorReceb = pd.concat([ValorReceb, nova_parcela_venda], ignore_index=True) 
                        vendasareceber.append(nova_parcela_venda)

                ## Verifica se o cliente existe na lista de clientes, se não, exibe mensagem de erro
        if Participante not in clientes["Nome"].values:
            print(f"Cliente {Participante} não encontrado na lista de clientes! Verifique se o cliente está cadastrado ou se o nome foi digitado corretamente.")            
    else:
        print(f"Produto não cadastrado no estoque! {produto} - {Tamanho}")
    return VendasT, estoque, ValorReceb, clientes