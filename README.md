# SISTEMA DE CONTROLE DE LOJA — PYTHON + EXCEL

DESCRIÇÃO
Sistema de controle para pequena loja desenvolvido em Python com integração direta com planilha Excel. O sistema lê o caixa diário registrado no Excel e processa automaticamente todas as operações, distribuindo os lançamentos nas abas de Estoque, Compras, Vendas, Contas a Receber e Contas a Pagar.

O objetivo é automatizar o controle operacional e reduzir erros de lançamento manual.

---

OBJETIVO DO PROJETO

Automatizar o processamento das operações diárias de uma loja pequena, centralizando:

* movimentações de caixa
* controle de estoque
* registro de compras
* registro de vendas
* contas a receber
* contas a pagar

Tudo a partir de um único lançamento diário no caixa.

---

FUNCIONAMENTO ATUAL

O sistema executa os seguintes passos:

1. Lê a aba "Caixa" da planilha Excel
2. Identifica cada tipo de operação registrada
3. Processa as regras de negócio em Python
4. Atualiza automaticamente as abas:

* Estoque
* Compras
* Vendas
* A receber
* A pagar

Todos os cálculos e validações são feitos no Python.

---

TECNOLOGIAS UTILIZADAS

* Python 3
* Pandas
* OpenPyXL / XlsxWriter
* Excel como base de dados
* Regras de negócio implementadas em Python

---

ESTRUTURA DO PROJETO (EXEMPLO)

loja-controle/

src/
lançamentodiario.py
validacoesexcel.py
dataframe.py
main.py
config.py
vendas.py
compras.py

data/
controle.xlsx

tests/

requirements.txt
.gitignore
README.md

---

COMO EXECUTAR

1. Clonar o repositório

git clone <url-do-repositorio>
cd loja-controle

2. Criar ambiente virtual (recomendado)

Windows:
python -m venv venv
venv\Scripts\activate

Linux/Mac:
python -m venv venv
source venv/bin/activate

3. Instalar dependências

pip install -r requirements.txt

4. Executar o sistema

python src/loja_python.py

---

ESTRUTURA ESPERADA DA PLANILHA

A planilha deve conter as abas:

* Caixa
* Estoque
* Compras
* Vendas
* A receber
* A pagar

ABA CAIXA — COLUNAS MÍNIMAS

Data
Nome do produto
Tipo operacao
Quantidade
Valor unitario
Forma pagamento
Observacoes

(Os nomes podem ser ajustados conforme o layout real.)

---

REGRAS DE NEGÓCIO IMPLEMENTADAS

* Verificação de produto existente no estoque
* Atualização automática de saldo
* Separação por tipo de operação
* Cálculo de totais de venda e compra
* Geração de contas a pagar e receber
* Consolidação de movimentações diárias

---

ROADMAP — EVOLUÇÃO FUTURA

Planejamento das próximas versões:

* Interface Web para lançamento de caixa
* Entrada de dados via página web
* Processamento em Python
* Gravação final no Excel
* Possível migração futura para banco de dados
* Dashboard de indicadores
* Relatórios automáticos
* Controle de usuários

---

ARQUITETURA FUTURA PLANEJADA

Interface Web (Caixa)
↓
API Python
↓
Regras de negócio
↓
Excel (base de dados)

---

TESTES

Testes automatizados em desenvolvimento:

* leitura de planilha
* validação de lançamentos
* consistência de estoque
* integridade de valores

---

LICENÇA

Uso para estudo e controle interno.
Licença futura sugerida: MIT.

---

AUTOR

Vinícius William Gomes Souza
Projeto de automação de controle de loja com Python + Excel.

---
