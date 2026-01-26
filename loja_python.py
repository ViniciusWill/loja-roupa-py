
import pandas as pd
import os as os
from datetime import datetime as data

nomearq = "Compras.xlsx"
Hoje = data.now()
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
        caixa.columns = caixa.columns.str.strip()
        return caixa
     except:
        print('Caixa não encontrado')

#LerComprasDiarias------------------------------------------ 
def Comprasdiarias():
    Estoqueanalise =  Estoque()
    Comprastotal = comprascalc()
    try:
        caixa = Caixa()

        if caixa is None:
         print("Caixa inválido")
         return
        
        comprasday =  caixa[caixa["Operação"] == "Compra"]

        for _, linha in comprasday.iterrows():
            produto = linha["Nome do produto"]
            Tamanho = linha["Tamanho"]
            qntd = linha["Quantidade"]
            condicao = (
                (Estoqueanalise["Nome do produto"] == produto) &
                (Estoqueanalise["Tamanho"] == Tamanho) 
            )
            if condicao.any():
                Estoqueanalise.loc[condicao, "Quantidade"] += qntd
                print(f"Produto encontrado no estoque: {produto} - {Tamanho}")
            else:
                print(f"Produto não encontrado no estoque: {produto} - {Tamanho}")

            if condicao.any():
                Comprastotal.loc[condicao, "Quantidade"] += qntd
                print(f"Produto encontrado nas compras: {produto} - {Tamanho}")
            else:
                print(f"Produto não encontrado na aba de compras: {produto} - {Tamanho}")

            abas = {"Caixa": pd.read_excel(nomearq, "Caixa"),
                    "Compras": pd.read_excel(nomearq, "Compras"),
                    "Vendas": pd.read_excel(nomearq, "Vendas"),
                    "Estoque": Estoqueanalise}
           

            with pd.ExcelWriter(nomearq, engine="openpyxl") as writer:
                    for nome, df in abas.items():      
                        df.to_excel(writer, sheet_name=nome, index=False)
    except Exception as e:
        print('Compras diarias não encontradas')
        print("Erro", e)

#LerVendasDiaria--------------------------------------------
def Vendasdiarias(caixa):
     try:    
        vendasday = caixa[caixa["Operação"] == "Venda"]
        return vendasday
     except:
        print('Vendas diarias não encontrads')

#LerEstoque-------------------------------------------------
def Estoque():
     try:
        estoque = pd.read_excel(nomearq, sheet_name="Estoque")
        estoque.columns = estoque.columns.str.strip()
        print('Estoque encontrado')
        return estoque
     except:
         print('Estoque não encontrado')



#ComprasTotal-------------------------------------------
def comprascalc():
    try:
        comp = pd.read_excel(nomearq, sheet_name="Compras")
        comp.columns = comp.columns.str.strip()
        print('Compra total encontrada')
        return comp
    except:
        print('Compras não encontradas')
#VendasTotal---------------------------------------------------
def vendascalc():
   try:
     vend = pd.read_excel(nomearq, sheet_name='Vendas')
     vend.columns = vend.columns.str.strip()
     print(vend)
     return vend
   except:
     print('Vendas não encontradas')

#Principal--------------------------------------------
print("Buscando Arquivo..")
Leitura = ler()

if Leitura == True:
    Caixa()
    Comprasdiarias()

