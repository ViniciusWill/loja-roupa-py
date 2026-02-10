
import pandas as pd
import os as os


nomearq = "Compras.xlsx"

#LerArquivo---------------------------------------------
def ler():
    if os.path.exists(nomearq):
        print("Arquivo encontrado")
        return True
    else:
        print("Arquivo não encontrado!")
        return False
#LerCaixaDiario---------------------------------------
def Caixa():
    try:
        print('Verificando caixa diario...')
        caixa = pd.read_excel(nomearq, sheet_name='Caixa')
        caixa = caixa.sort_values("Data")
        caixa.columns = caixa.columns.str.strip()
        print('Caixa encontrado')
        return caixa

    except Exception as e:
        print('Caixa não encontrado')
        print(e)
        return pd.DataFrame()
#LerEstoque-------------------------------------------------
def Estoque():
     try:
        estoque = pd.read_excel(nomearq, sheet_name="Estoque")
        estoque.columns = estoque.columns.str.strip()
        print('Estoque encontrado')
        return estoque
     except:
         print('Estoque não encontrado')

#LerComprasEvendasTotal---------------------------------------
def comptotal():
    try:
        compras = pd.read_excel(nomearq, sheet_name="Compras")
        compras.columns = compras.columns.str.strip()
        print('Compras Totais encontradas')
        return compras
    except Exception as e:
        print('Compras Totais não encontradas!')
        print(f'Erro: {e}')


def vendtotal():
    try:
        vendas = pd.read_excel(nomearq, sheet_name="Vendas")
        vendas.columns = vendas.columns.str.strip()
        print('Vendas totais encontradas')
        return vendas
    except Exception as e:
        print('Vendas totais não encontradas')
        print(f'Erro: {e}')

#LançarOperacoesDiarias----------------------------------------
def lancaropdia():
    caixa = Caixa()
    estoque = Estoque()
    comprast = comptotal()
    vendast = vendtotal()
    novoprod = []
    vendasdiarias = []
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

        condicao = ( (estoque["Nome do produto"] == produto) & 
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
                else:
                    print('Não há unidades do produto disponiveis para venda!')
            else:
                print(f"Produto não cadastrado no estoque! {produto} - {Tamanho}")
    
        else:
              print(f"Foi encontrado uma operação invalida, verifique as operações lançadas no caixa! Operação: {operacao}!")
        
    
        with pd.ExcelWriter(nomearq, mode="a", if_sheet_exists='replace', engine="openpyxl") as writer:
                estoque.to_excel(writer, sheet_name="Estoque", index=False)
                comprast.to_excel(writer, sheet_name="Compras", index=False)
         
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
    print("operações diarias lançadas com sucesso! Limpando caixa...")
    caixa_limpo = pd.DataFrame(columns=caixa.columns)
    with pd.ExcelWriter(nomearq, mode="a", if_sheet_exists='replace', engine="openpyxl") as writer:
     caixa_limpo.to_excel(writer, sheet_name="Caixa", index=False)
    print("Caixa limpo com sucesso!")

#Principal--------------------------------------------


print("Buscando Arquivo..")
Leitura = ler()
if Leitura == True:
    lancaropdia()
   