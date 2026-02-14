import pandas as pd
import os
from config import ARQUIVO_EXCEL


def encontrar_arquivo():
    if os.path.exists(ARQUIVO_EXCEL):
        print("Arquivo encontrado.")
        return ARQUIVO_EXCEL
    else:
        print("Arquivo não encontrado.")   
        return pd.DataFrame()
       

#LerCaixaDiario---------------------------------------
def Caixa():
    try:
        caixa = pd.read_excel(ARQUIVO_EXCEL, sheet_name='Caixa')
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
        estoque = pd.read_excel(ARQUIVO_EXCEL, sheet_name="Estoque")
        estoque.columns = estoque.columns.str.strip()
        print('Estoque encontrado')
        return estoque
     except Exception as e:
         print('Estoque não encontrado')
         print(e)
         return pd.DataFrame()


#LerComprasEvendasTotal---------------------------------------
def comptotal():
    try:
        compras = pd.read_excel(ARQUIVO_EXCEL, sheet_name="Compras")
        compras.columns = compras.columns.str.strip()
        print('Compras Totais encontradas')
        return compras
    except Exception as e:
        print('Compras Totais não encontradas!')
        print(f'Erro: {e}')
        return pd.DataFrame()

def vendtotal():
    try:
        vendas = pd.read_excel(ARQUIVO_EXCEL, sheet_name="Vendas")
        vendas.columns = vendas.columns.str.strip()
        print('Vendas totais encontradas')
        return vendas
    except Exception as e:
        print('Vendas totais não encontradas')
        print(f'Erro: {e}')
        return pd.DataFrame()

#LerValoresaReceberePagar---------------------------------------
def valreceb():
    try: 
        valreceber = pd.read_excel(ARQUIVO_EXCEL, sheet_name = "A receber")
        valreceber.columns = valreceber.columns.str.strip()
        print('Valores a receber encontrados')
        return valreceber
    except Exception as e:
        print('Valores a receber não encontrados')
        print(f'Erro: {e}')
        return pd.DataFrame()
def valpagar():
    try: 
        valrpag = pd.read_excel(ARQUIVO_EXCEL, sheet_name= "A pagar")
        valrpag.columns = valrpag.columns.str.strip()
        print('Valores a pagar encontrados')
        return valrpag
    except Exception as e:
        print('Valores a pagar não encontrados')
        print(f'Erro: {e}')
        return pd.DataFrame()
def Clientes():
    try:
        clientes = pd.read_excel(ARQUIVO_EXCEL, sheet_name="Clientes")
        clientes.columns = clientes.columns.str.strip()
        print('Clientes encontrados')
        return clientes
    except Exception as e:
        print('Clientes não encontrados')
        print(f'Erro: {e}')
        return pd.DataFrame()


def executar_validacoes():
    encontrar_arquivo()
    df_caixa = Caixa()
    df_estoque = Estoque()
    df_comptotal = comptotal()
    df_vendtotal = vendtotal()
    df_valreceb = valreceb()
    df_valpagar = valpagar()
    df_clientes = Clientes()

    return {
        "caixa": df_caixa,
        "estoque": df_estoque,
        "compras": df_comptotal,
        "vendas": df_vendtotal,
        "valoreb": df_valreceb,
        "valorpag": df_valpagar,
        "nomearq": ARQUIVO_EXCEL,
        "clientes": df_clientes
    }



