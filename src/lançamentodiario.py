import pandas as pd 
from dataframe import Dataframescompra, DataframesEstoque, Dataframesvenda
from compras import Lançarcomprasnoestoque
from vendas import Lançarvendasnoestoque


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
    
        
        ##  cria dataframes para registrar as compras, vendas, contas a pagar e contas a receber

        NovaVenda = Dataframesvenda(Participante, produto, Tamanho, sexo, qnt, valoruni, data)
                
        if operacao == "Compra":
            CompTotal = Lançarcomprasnoestoque(linha, estoque, ComprasTotal, dados)
#         elif operacao == "Venda":
#                 ## se o produto existe no estoque, atualiza a quantidade
#             if condicao.any():
#                 qntattest = estoque.loc[condicao, "Quantidade"].iloc[0] - qnt
#                 ## verifica se há unidades disponiveis para venda, se sim, atualiza o estoque e registra a venda, se não, exibe mensagem de erro
#                 if qntattest >= 0:
#                      estoque.loc[condicao, "Quantidade"] = qntattest
                      
#                      vendast = Lançarvendasnoestoque(vendast, NovaVenda) 
#                      vendasdiarias.append(NovaVenda)    
#                 elif qntattest < 0:
#                     print('Não há unidades do produto disponiveis para venda!')
        
#                 if Pagamento == "Parcelado":    
#                         valor_total = valorven * qnt
#                         valor_parcela = valor_total / Parcelas
#                         for i in range(Parcelas):
#                             totalatualizado = valor_total - (valor_parcela * i)
#                             vencimento = data + pd.DateOffset(months=i+1)
#                             nova_parcela_venda = pd.DataFrame([{ "Cliente": Participante,
#                                                           "Nome do produto": produto,
#                                                           "Parcela": i+1,
#                                                           "Valor parcela": valor_parcela,
#                                                           "Valor total": valor_total, 
#                                                           "Valor total pendente": totalatualizado,
#                                                           "Data vencimento": vencimento,}])
#                             if valoreb.empty:
#                                 valoreb = nova_parcela_venda
#                             else:
#                                 valoreb = pd.concat([valoreb, nova_parcela_venda], ignore_index=True) 
#                         vendasareceber.append(nova_parcela_venda)

#                 ## Verifica se o cliente existe na lista de clientes, se não, exibe mensagem de erro
#                 if Participante not in clientes["Nome"].values:
#                     print(f"Cliente {Participante} não encontrado na lista de clientes! Verifique se o cliente está cadastrado ou se o nome foi digitado corretamente.")
                
                
#             else:
#                 print(f"Produto não cadastrado no estoque! {produto} - {Tamanho}")
               
#         else:
#               print(f"Foi encontrado uma operação invalida, verifique as operações lançadas no caixa! Operação: {operacao}!")
         

#     with pd.ExcelWriter(nomearq, mode="a", if_sheet_exists='replace', engine="openpyxl") as writer:
# #                 estoque.to_excel(writer, sheet_name="Estoque", index=False)
#                 ComprasTotal.to_excel(writer, sheet_name="Compras", index=False)
#                 valoreb.to_excel(writer, sheet_name="A Receber", index=False)
#                 valorpag.to_excel(writer, sheet_name="A Pagar", index=False)
#                 vendast.to_excel(writer, sheet_name="Vendas", index=False)
    
#     dados["Estoque"] = estoque
#     dados["Compras"] = ComprasTotal
#     dados["A Receber"] = valoreb
#     dados["A Pagar"] = valorpag
#     dados["Vendas"] = vendast
# # Relatorio de compras 
#     if novoprod:
#       novoprod = pd.concat(novoprod, ignore_index=True)
#     else:
#      novoprod = pd.DataFrame()

#     if not novoprod.empty:
#         print("Os novos produtos cadastrados foram:")
#     for _, prod in novoprod.iterrows():
#         nome = prod["Nome do produto"]
#         tamanho = prod["Tamanho"]
#         print(f"{nome} - {tamanho}")
#     else:
#         print("Nenhum novo produto foi cadastrado no estoque.")

# # Relatorio de vendas
#     if vendasdiarias:
#         novavenda = pd.concat(vendasdiarias, ignore_index=True)
#     else:
#         novavenda = pd.DataFrame()

#     if not novavenda.empty:
#         print("As vendas realizadas foram:")
#     for _, vend in novavenda.iterrows():
#         nome = vend["Nome do produto"]
#         tamanho = vend["Tamanho"]
#         data = vend["Data"]
#         print(f"{nome} - {tamanho} - Data: {data}")
#     else:
#         print("Nenhuma venda foi realizada hoje.")

#  ## limpar caixa diario
# def limparcaixa(dados):
#     caixa = dados["Caixa"]
#     nomearq = dados["nomearq"]
#     print("operações diarias lançadas com sucesso! Limpando caixa...")
#     caixa_limpo = pd.DataFrame(columns=dados["Caixa"].columns)
#     with pd.ExcelWriter(nomearq, mode="a", if_sheet_exists='replace', engine="openpyxl") as writer:
#      caixa_limpo.to_excel(writer, sheet_name="Caixa", index=False)
#     print("Caixa limpo com sucesso!")


