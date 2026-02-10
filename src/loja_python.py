
import pandas as pd
import os as os
from validacoesexcel import executar_validacoes


#LançarOperacoesDiarias----------------------------------------
def lancaropdia(dados):
    caixa = dados["caixa"]
    estoque = dados["estoque"]
    comprast = dados["compras"]
    vendast = dados["vendas"]
    nomearq = dados["nomearq"]
    valoreb = dados["valoreb"]
    novoprod = []
    vendasdiarias = []
    vendasareceber = []
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
    

        condicao = ((estoque["Nome do produto"] == produto) & 
                    (estoque["Tamanho"] == Tamanho))
        if operacao == "Compra":
            ##se o produto já existe no estoque, atualiza a quantidade
            if condicao.any():
                
                qntattest = estoque.loc[condicao, "Quantidade"].iloc[0] + qnt
                estoque.loc[condicao, "Quantidade"] = qntattest
          

                novacomp = pd.DataFrame([{"Nome do produto": produto, 
                                        "Tamanho": Tamanho,
                                        "Quantidade": qnt,
                                        "Valor unitario compra": valoruni,
                                        "Data da compra": data,
                                        "Sexo": sexo }])

                comprast = pd.concat([comprast, novacomp], ignore_index=True)
            ##se o produto não existe no estoque, cadastra o produto e a compra
            else:
    
                novoitem = pd.DataFrame([{"Nome do produto": produto, 
                                           "Tamanho": Tamanho,
                                            "Quantidade": qnt, 
                                            "Valor unitario compra": valoruni,
                                            "Data da compra": data,
                                            "Sexo": sexo
                                             }])
            
                linha_estoque = pd.DataFrame([[produto, Tamanho, qnt, valoruni]], 
                                             columns=["Nome do produto", "Tamanho", "Quantidade", "Valor unitario"])
                estoque = pd.concat([estoque, linha_estoque], ignore_index=True)
                comprast = pd.concat([comprast, novoitem], ignore_index=True)
                novoprod.append(novoitem)
        elif operacao == "Venda":
                ##se o produto existe no estoque, atualiza a quantidade
            if condicao.any():
                qntattest = estoque.loc[condicao, "Quantidade"].iloc[0] - qnt
                ## verifica se há unidades disponiveis para venda, se sim, atualiza o estoque e registra a venda, se não, exibe mensagem de erro
                if qntattest >= 0:
                     estoque.loc[condicao, "Quantidade"] = qntattest
                     novavendaT = pd.DataFrame([{"Nome do produto": produto,
                                           "Tamanho": Tamanho,
                                           "Quantidade": qnt,
                                           "Valor unitario venda": valorven,
                                            "Data": data,
                                             "Sexo": sexo }])           
                     novavenda = pd.concat([vendast,novavendaT], ignore_index=True)
                     vendasdiarias.append(novavendaT)  # Adiciona a venda diária à lista
                if Pagamento == "Parcelado":    
                        valor_total = valorven * qnt
                        valor_parcela = valor_total / Parcelas
                        for i in range(Parcelas):
                            vencimento = data + pd.DateOffset(months=i+1)
                            nova_parcela = pd.DataFrame([{ "Cliente": Participante,
                                                          "Nome do produto": produto,
                                                          "Parcela": i+1,
                                                          "Valor parcela": valor_parcela,
                                                          "Data": vencimento,
                                                          "Valor total": valor_total}])
                            valoreb = pd.concat([valoreb, nova_parcela], ignore_index=True)
                            vendasareceber.append(nova_parcela)  
                else:
                    print('Não há unidades do produto disponiveis para venda!')
            else:
                print(f"Produto não cadastrado no estoque! {produto} - {Tamanho}")
    
        else:
              print(f"Foi encontrado uma operação invalida, verifique as operações lançadas no caixa! Operação: {operacao}!")
        
    
        with pd.ExcelWriter(nomearq, mode="a", if_sheet_exists='replace', engine="openpyxl") as writer:
                estoque.to_excel(writer, sheet_name="Estoque", index=False)
                comprast.to_excel(writer, sheet_name="Compras", index=False)
                valoreb.to_excel(writer, sheet_name="A receber", index=False)
         
    ## --- Relatorio de compras 
    if novoprod: 
        novacomp = pd.concat(novoprod, ignore_index=True)
    else:
        novacomp = pd.DataFrame()

    if not novacomp.empty:
      print("Os novos produtos cadastrados foram:")
      for _,prod in novoprod.iterrows():
        nome = prod["Nome do produto"]
        tamanho = prod["Tamanho"]
        print(f"{nome} - {tamanho} ")
    else: 
        print("Nenhum novo produto foi cadastrado no estoque.")
    ## --- Relatorio de vendas
    if vendasdiarias:  # Verifica se a lista de vendas diárias não está vazia
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
    ##LimparCaixa
    ##print("operações diarias lançadas com sucesso! Limpando caixa...")
    ##caixa_limpo = pd.DataFrame(columns=caixa.columns)
    ##with pd.ExcelWriter(nomearq, mode="a", if_sheet_exists='replace', engine="openpyxl") as writer:
     ##caixa_limpo.to_excel(writer, sheet_name="Caixa", index=False)
    ##print("Caixa limpo com sucesso!")



#Principal--------------------------------------------
if __name__ == "__main__":
    print("Iniciando sistema...")
    
    # 1. Busca os dados
    dados_do_excel = executar_validacoes()
    
    # 2. Pega a tabela do caixa para analisar
    tabela_caixa = dados_do_excel["caixa"]

    # 3. Diagnóstico detalhado
    if tabela_caixa is None:
        print("ERRO CRÍTICO: Ocorreu um erro ao tentar ler a aba Caixa (verifique se o arquivo está fechado ou corrompido).")
    
    elif tabela_caixa.empty:
        print("AVISO: A aba 'Caixa' foi encontrada, mas está VAZIA (0 linhas de dados).")
        print("Adicione pelo menos uma linha de venda ou compra no Excel para processar.")
    
    else:
        # Só entra aqui se tiver dados de verdade
        print(f"Sucesso! Encontrei {len(tabela_caixa)} operações no caixa.")
        print("Iniciando processamento...")
        lancaropdia(dados_do_excel)
        print("Processo finalizado com sucesso!")