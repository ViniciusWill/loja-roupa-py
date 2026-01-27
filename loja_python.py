
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
    try:
        caixa = Caixa()

        if caixa is None:
         print("Caixa inválido")
         return
        comprasday =  caixa[caixa["Operação"] == "Compra"]
        return comprasday
    except Exception as e:
        print('Compras diarias não encontradas')
        print("Erro", e)

#LerVendasDiaria--------------------------------------------
def Vendasdiarias():
     try:    
        caixa = Caixa()
        if caixa is None:
            print("Caixa invalido")
            return
        vendasday = caixa[caixa["Operação"] == "Venda"]
        return vendasday
     except Exception as e:
        print('Vendas diarias não encontrads')
        print("Erro", e)
#LerEstoque-------------------------------------------------
def Estoque():
     try:
        estoque = pd.read_excel(nomearq, sheet_name="Estoque")
        estoque.columns = estoque.columns.str.strip()
        print('Estoque encontrado')
        return estoque
     except:
         print('Estoque não encontrado')

#LançarComprasDiarias----------------------------------------
def lancarcompdia():
    estoque = Estoque()
    comprasdias = Comprasdiarias()
    print(comprasdias)

    for _,linha in comprasdias.iterrows():
        print = linha[""]


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
