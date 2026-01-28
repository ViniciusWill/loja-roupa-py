
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
        print('Compras diarias encontradas.')
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
        print('Vendas diarias encontradas.')
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
    print('Verificando produtos que estão no estoque..')
    for _,linha in comprasdias.iterrows():
        produto = linha["Nome do produto"] 
        Tamanho = linha["Tamanho"] 
        qntcomp = linha["Quantidade"]
    
        condicaocomp = ( (estoque["Nome do produto"] == produto) & 
                    (estoque["Tamanho"] == Tamanho))
        if condicaocomp.any():
            qntatt = estoque.loc[condicaocomp, "Quantidade"].iloc[0] + qntcomp
            print(f"Produto encontrado: {produto} - {Tamanho}")
            print(f"Produto no estoque após compra: {produto} - {Tamanho} - Unidades: {qntatt}")

        else:
            print(f"Produto não encontrado: {produto} - {Tamanho}")

#LançarVendasDiarias-------------------------------------------
def lancarvendia():
    estoque = Estoque()
    vendia = Vendasdiarias()
    print(vendia)
    print('Verificando estoque dos produtos vendidos..')
    for _,linha in vendia.iterrows():
        produto = linha["Nome do produto"]
        Tamanho = linha["Tamanho"]
        qntdvend = linha["Quantidade"]
        condicaovenda = ( (estoque["Nome do produto"] == produto) &
                           (estoque["Tamanho"] == Tamanho))
        
        if condicaovenda.any(): 
            qntatt = estoque.loc[condicaovenda, "Quantidade"].iloc[0] - qntdvend
            print(f"Produto encontrado no estoque: {produto} - {Tamanho}")
            print(f"Produto no estoque após venda: {produto} - {Tamanho} - Unidades: {qntatt} ") 
        else:
            print(f"Atenção! O produto vendido não está cadastrado no estoque! {produto} - {Tamanho}")



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
    Comprasdiarias()
    lancarcompdia()
    lancarvendia()
    