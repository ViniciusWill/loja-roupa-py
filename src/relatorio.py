import pandas as pd 
# Relatorio de compras 
def RelatorioCompras(novoprod):

    if novoprod:
      novoprod = pd.concat(novoprod, ignore_index=True)
    else:
       novoprod = pd.DataFrame()
 
    if not novoprod.empty:
        print("Os novos produtos cadastrados foram:")
        for _, prod in novoprod.iterrows():
         nome = prod["Nome do produto"]
         tamanho = prod["Tamanho"]
         print(f"{nome} - {tamanho}")
    else:
        print("Nenhum novo produto foi cadastrado no estoque.")

# Relatorio de vendas
def RelatoriosVendas(vendad):
    if vendad:
        vendad = pd.concat(vendad, ignore_index=True)
    else:
        vendad = pd.DataFrame()

    if not vendad.empty:
        print("As vendas realizadas foram:")
        for _, vend in vendad.iterrows():
            nome = vend["Nome do produto"]
            tamanho = vend["Tamanho"]
            data = vend["Data"]
            print(f"{nome} - {tamanho} - Data: {data}")
    else:
        print("Nenhuma venda foi realizada hoje.")