from validacoesexcel import executar_validacoes
from formatarexcel import executar_formatacao
from lançamentodiario import lancaropdia


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
        executar_formatacao(dados_do_excel)
        print("Formatações aplicadas com sucesso! ")
        # limpar = input("Deseja limpar o caixa? (Digite 's' para sim ou 'n' para não): ")
        # if limpar.lower() == "s":
        #     limparcaixa(dados_do_excel)
        # else:            
        #     print("Caixa não limpo. Lembre-se de limpar o caixa manualmente ou executar a função de limpeza para evitar processar as mesmas operações novamente.")
