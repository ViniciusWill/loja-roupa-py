
import pandas as pd
import os as os
from validacoesexcel import executar_validacoes
from formatarexcel import executar_formatacao

##  LançarOperacoesDiarias
def lancaropdia(dados):
    caixa = dados["Caixa"]
    estoque = dados["Estoque"]
    ComprasTotal = dados["Compras"]
    vendast = dados["Vendas"]
    nomearq = dados["nomearq"]
    valoreb = dados["A Receber"]
    valorpag = dados["A Pagar"]
    clientes = dados["Clientes"]
    novoprod = []
    vendasdiarias = []
    vendasareceber = []
    contasapagar = []
    print('Verificando produtos que estão no estoque..')
    for _,linha in caixa.iterrows():
        produto = linha["Nome do produto"] 
        Tamanho = linha["Tamanho"] 
        qnt = linha["Quantidade"]
        valoruni = linha["Valor unitario compra"]
        valorven = linha["Valor unitario venda"]
        operacao = linha["Operação"]
        data = linha["Data"]
        sexo = linha["Sexo"]
        Pagamento = linha["Forma Pag"]
        Parcelas = linha["Parcelas"]
        Participante = linha["Participante"]  
    
        ## verifica se o produto existe no estoque 
        condicao = ((estoque["Nome do produto"] == produto) & 
                    (estoque["Tamanho"] == Tamanho))

        ##  cria dataframes para registrar as compras, vendas, contas a pagar e contas a receber
        NovaCompra = pd.DataFrame([{"Nome do produto": produto, 
                                    "Tamanho": Tamanho,
                                    "Sexo": sexo,
                                    "Quantidade": qnt,
                                    "Valor unitario compra": valoruni,
                                    "Data da compra": data
                                    }])
        NovoItemCompraEstoque = pd.DataFrame([{"Nome do produto": produto, 
                                           "Tamanho": Tamanho, 
                                           "Sexo": sexo,
                                            "Quantidade": qnt, 
                                            "Valor unitario compra": valoruni,
                                            "Data da compra": data
                                           
                                             }])
        NovaLinhaEstoque = pd.DataFrame([[produto, Tamanho, qnt, valoruni]],
                    columns=["Nome do produto", "Tamanho", "Quantidade", "Valor unitario compra"])         

        NovaVenda = pd.DataFrame([{ "Cliente": Participante,
                                           "Nome do produto": produto,
                                           "Tamanho": Tamanho,  
                                           "Sexo": sexo,
                                           "Quantidade": qnt,
                                           "Valor unitario venda": valorven,
                                            "Data": data
                                             }])  
                
        if operacao == "Compra":
            ## se o produto já existe no estoque, atualiza a quantidade
            if condicao.any():
                    qntattest = estoque.loc[condicao, "Quantidade"].iloc[0] + qnt
                    estoque.loc[condicao, "Quantidade"] = qntattest
                    ComprasTotal = pd.concat([ComprasTotal, NovaCompra], ignore_index=True)
            ## se o produto não existe no estoque, cadastra o produto e a compra
            else:
                    estoque = pd.concat([estoque, NovaLinhaEstoque], ignore_index=True)
                    ComprasTotal = pd.concat([ComprasTotal, NovoItemCompraEstoque], ignore_index=True)
                    novoprod.append(NovoItemCompraEstoque)
            ## se a compra for parcelada, calcula as parcelas e registra as contas a pagar
            if Pagamento == "Parcelado":
                valor_total = valoruni * qnt
                valor_parcela = valor_total / Parcelas
                for i in range(Parcelas):
                    totalatualizado = valor_total - (valor_parcela * i)
                    vencimento = data + pd.DateOffset(months=i+1)
                    nova_parcela_compra = pd.DataFrame([{ "Participante": Participante,
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

        elif operacao == "Venda":
                ## se o produto existe no estoque, atualiza a quantidade
            if condicao.any():
                qntattest = estoque.loc[condicao, "Quantidade"].iloc[0] - qnt
                ## verifica se há unidades disponiveis para venda, se sim, atualiza o estoque e registra a venda, se não, exibe mensagem de erro
                if qntattest >= 0:
                     estoque.loc[condicao, "Quantidade"] = qntattest
                      
                     vendast = pd.concat([vendast,NovaVenda], ignore_index=True)
                     vendasdiarias.append(NovaVenda) 
                elif qntattest < 0:
                    print('Não há unidades do produto disponiveis para venda!')
                    vendast = pd.DataFrame()  
                if Pagamento == "Parcelado":    
                        valor_total = valorven * qnt
                        valor_parcela = valor_total / Parcelas
                        for i in range(Parcelas):
                            totalatualizado = valor_total - (valor_parcela * i)
                            vencimento = data + pd.DateOffset(months=i+1)
                            nova_parcela_venda = pd.DataFrame([{ "Cliente": Participante,
                                                          "Nome do produto": produto,
                                                          "Parcela": i+1,
                                                          "Valor parcela": valor_parcela,
                                                          "Valor total": valor_total, 
                                                          "Valor total pendente": totalatualizado,
                                                          "Data vencimento": vencimento,}])
                            if valoreb.empty:
                                valoreb = nova_parcela_venda
                            else:
                                valoreb = pd.concat([valoreb, nova_parcela_venda], ignore_index=True) 
                        vendasareceber.append(nova_parcela_venda)

                ## Verifica se o cliente existe na lista de clientes, se não, exibe mensagem de erro
                if Participante not in clientes["Nome"].values:
                    print(f"Cliente {Participante} não encontrado na lista de clientes! Verifique se o cliente está cadastrado ou se o nome foi digitado corretamente.")
                
                
            else:
                print(f"Produto não cadastrado no estoque! {produto} - {Tamanho}")
                vendast = pd.DataFrame()  
        else:
              print(f"Foi encontrado uma operação invalida, verifique as operações lançadas no caixa! Operação: {operacao}!")
              vendast = pd.DataFrame()  
        with pd.ExcelWriter(nomearq, mode="a", if_sheet_exists='replace', engine="openpyxl") as writer:
                estoque.to_excel(writer, sheet_name="Estoque", index=False)
                ComprasTotal.to_excel(writer, sheet_name="Compras", index=False)
                valoreb.to_excel(writer, sheet_name="A Receber", index=False)
                valorpag.to_excel(writer, sheet_name="A Pagar", index=False)
                vendast.to_excel(writer, sheet_name="Vendas", index=False)

##  Relatorio de compras 
    if novoprod: 
        NovaCompra = pd.concat(novoprod, ignore_index=True)
    else:
        NovaCompra = pd.DataFrame()

    if not NovaCompra.empty:
      print("Os novos produtos cadastrados foram:")
      for _,prod in novoprod.iterrows():
        nome = prod["Nome do produto"]
        tamanho = prod["Tamanho"]
        print(f"{nome} - {tamanho} ")
    else: 
        print("Nenhum novo produto foi cadastrado no estoque.")
##  Relatorio de vendas
    if vendasdiarias:  #
        novavenda = pd.concat(vendasdiarias, ignore_index=True)
    else:
        novavenda = pd.DataFrame()

    if not novavenda.empty:   
        print("As vendas realizadas foram:")
        for _,vend in novavenda.iterrows():
            nome = vend["Nome do produto"]
            tamanho = vend["Tamanho"]
            data = vend["Data"]
            print(f"{nome} - {tamanho} - Data: {data}")
    else:
        print("Nenhuma venda foi realizada hoje.")

 ## limpar caixa diario
def limparcaixa(dados):
    caixa = dados["Caixa"]
    nomearq = dados["nomearq"]
    print("operações diarias lançadas com sucesso! Limpando caixa...")
    caixa_limpo = pd.DataFrame(columns=dados["Caixa"].columns)
    with pd.ExcelWriter(nomearq, mode="a", if_sheet_exists='replace', engine="openpyxl") as writer:
     caixa_limpo.to_excel(writer, sheet_name="Caixa", index=False)
    print("Caixa limpo com sucesso!")



## Principal
if __name__ == "__main__":
    print("Iniciando sistema...")
    
    dados_do_excel = executar_validacoes()
    tabela_caixa = dados_do_excel["Caixa"]

    if tabela_caixa is None:
        print("ERRO CRÍTICO: Ocorreu um erro ao tentar ler a aba Caixa (verifique se o arquivo está fechado ou corrompido).")
    
    elif tabela_caixa.empty:
        print("AVISO: A aba 'Caixa' foi encontrada, mas está VAZIA (0 linhas de dados).")
        print("Adicione pelo menos uma linha de venda ou compra no Excel para processar.")

    else:
        print("Iniciando processamento...")
        lancaropdia(dados_do_excel)
        print("Processo finalizado com sucesso!")
        print("Aplicando formatações finais no Excel...")
        executar_formatacao()
        print("Formatações aplicadas com sucesso! ")
        limpar = input("Deseja limpar o caixa? (Digite 's' para sim ou 'n' para não): ")
        if limpar.lower() == "s":
            limparcaixa(dados_do_excel)
        else:            
            print("Caixa não limpo. Lembre-se de limpar o caixa manualmente ou executar a função de limpeza para evitar processar as mesmas operações novamente.")
