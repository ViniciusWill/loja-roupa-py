
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
    novoprod = pd.DataFrame(columns=["Nome do produto", 
                                           "Tamanho",
                                            "Quantidade", 
                                            "Valor unitario compra"
                                             ])
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
            if condicao.any():
                
                qntattest = estoque.loc[condicao, "Quantidade"].iloc[0] + qnt
                estoque.loc[condicao, "Quantidade"] = qntattest
                # print(f"Produto encontrado: {produto} - {Tamanho} - {qnt}")
                # print(f"Produto no estoque após compra: {produto} - {Tamanho} - Unidades: {qntattest}")
                
                novacomp = pd.DataFrame([{"Nome do produto": produto, 
                                        "Tamanho": Tamanho,
                                        "Quantidade": qnt,
                                        "Valor unitario compra": valoruni,
                                        "Data da compra": data,
                                        "Sexo": sexo }])

                comprast = pd.concat([comprast, novacomp], ignore_index=True)
            else:
                novoprod.loc[len(novoprod)] = [
                produto,
                Tamanho,
                qnt, 
                valoruni]
                novacompT = pd.DataFrame([{"Nome do produto": produto, 
                                           "Tamanho": Tamanho,
                                            "Quantidade": qnt, 
                                            "Valor unitario compra": valoruni,
                                            "Data da compra": data,
                                            "Sexo": sexo
                                             }])
                estoque = pd.concat([estoque, novoprod], ignore_index=True)
                novacomp = pd.concat([comprast, novacompT], ignore_index=True)
        elif operacao == "Venda":
            if condicao.any():
                qntattest = estoque.loc[condicao, "Quantidade"].iloc[0] - qnt
                if qntattest >= 0:
                     estoque.loc[condicao, "Quantidade"] = qntattest
                    #  print(f"Produto encontrado: {produto} - {Tamanho}")
                    #  print(f"Produto no estoque após venda: {produto} - {Tamanho} - {qntattest}")
                     novavendaT = pd.DataFrame([{"Nome do produto": produto,
                                           "Tamanho": Tamanho,
                                           "Quantidade": qnt,
                                           "Valor unitario venda": valorven,
                                            "Data": data,
                                             "Sexo": sexo }])
                     novavenda = pd.concat([vendast,novavendaT], ignore_index=True)
                else:
                    print('Não há unidades do produto disponiveis para venda!')
            else:
                print(f"Produto não cadastrado no estoque! {produto} - {Tamanho}")
    
        else:
              print(f"Foi encontrado uma operação invalida, verifique as operações lançadas no caixa! Operação: {operacao}!")
    
        with pd.ExcelWriter(nomearq, mode="a", if_sheet_exists='replace', engine="openpyxl") as writer:
                estoque.to_excel(writer, sheet_name="Estoque", index=False)
                comprast.to_excel(writer, sheet_name="Compras", index=False)
 
    print("As Novas compras cadastradas foram:")
    for _,prod in novoprod.iterrows():
        nome = prod["Nome do produto"]
        tamanho = prod["Tamanho"]
        print(f"{nome} - {tamanho} ")
#Principal--------------------------------------------
print("Buscando Arquivo..")
Leitura = ler()
if Leitura == True:
    lancaropdia()
   