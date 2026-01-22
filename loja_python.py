import pandas as pd
import os as os
import openpyxl as op

#Menu Inicial------------------------------------------------
def opcoes():
    print('Escolha uma opção: ')
    print('1 - Cadastrar Produto ')
    print('2 - Verificar Estoque')
    print('3 - Sair')

#Cadastrar Produtos------------------------------------------------
def cadastrar():
    while True:
        nome = input('Nome do produto: ')
        tamanho = input('Tamanho: ')
        sexo = input('Sexo: ')
        precocompra = input('Preço de Compra unitário:')
        precovenda = input('Preço de Venda unitario: ')
        print('Confira as informações:')
        print(f"Nome: {nome} | Tamanho: {tamanho} | Sexo: {sexo}")
        print(f"Preço de compra unitario: {precocompra} | Preço de venda unitario: {precovenda}")
        infocorreta = input('\n(As informações estão corretas? (S-Sim / N-Não): ')
        infocorreta = infocorreta.upper()
        if infocorreta == 'S' :
            return True
        elif infocorreta == 'N':
             while True:
                opcao = input('Deseja reiniciar o cadastro? (S-Sim / N-Não): ')
                opcao = opcao.upper()
                if opcao == 'S':
                    print('Reiniciando cadastro..')
                    break
                elif opcao == 'N':
                    return False
        else:
            print('Opção invalida!')


#Ler_compras---------------------------------------------
def ler():
    nomearq = "Compras.xlsx"
    if os.path.exists(nomearq):
        comp = pd.read_excel(nomearq)
        print("Arquivo encontrado")
        comp.head()
        print(comp)
    while True:
        print('Insira uma opção: \n 1 - Verificar Produtos Masculinos \n 2 - Verificar produtos Femininos\n 3 - Voltar')
        opcaoest = input("Qual opçaõ voce deseja? ")
        if opcaoest == '1':
            print ('Os produtos masculinos são...')
            if  voltar ():
                return True
        elif opcaoest == '2':
            print ('Os produtos masculinos são...')
            if  voltar ():
                return True
        elif opcaoest == '3':
            print('Retornando a tela inicial..')        
            if voltar():
                return True
        else:
            print ("Opção invalida!")
            continue
    else:
        print("Arquivo não encontrado!")

#Voltar para inicio-----------------------
def voltar():
    while True:
        opcaovolt = input('Deseja voltar a tela inicial? (S- Sim / N - Não?)')
        opcaovolt = opcaovolt.upper()
        if opcaovolt == 'S':
            return True
        elif opcaovolt == 'N':
            return False
        else:   
            print('Opção Invalida')
            
            
#Principal------------------------------------------------

while True:
        opcoes()
        opcao = int(input('Insira uma opção:'))
        if opcao == 1:
                print('Voce selecionou a opção 1')
                verificacao = cadastrar()
                if verificacao == True:
                    print('Produto cadastrado com sucesso!')
                else:
                    print('Cadastro cancelado!')
                    continue             
        elif opcao == 2:
            print('Voce selecionou a opcao 2')
            ler()
     
        elif opcao == 3:
            print('Fim!')
            break
        else:
            print('Opcao invalida')
            continue
        
        

