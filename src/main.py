from validacoesexcel import executar_validacoes
from formatarexcel import executar_formatacao
from lançamentodiario import lancaropdia
from relatorio import RelatorioCompras, RelatoriosVendas


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
        dados_prontos, caminho_do_arquivo, DadosRelatorioCompras, DadosRelatoriosVendas = lancaropdia(dados_do_excel)
        print("Processo finalizado com sucesso!")
        print("Aplicando formatações finais no Excel...")
        executar_formatacao(dados_prontos)
        print("Formatações aplicadas com sucesso! ")
        print("Gerando relatorios de movimentações diarias...")
        RelatorioCompras(DadosRelatorioCompras) 
        RelatoriosVendas(DadosRelatoriosVendas)