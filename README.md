# Sistema ERP para Loja de Roupas

Aplicacao web em Flask para controle operacional e financeiro de uma loja de roupas.

O sistema cobre:
- vendas
- compras
- estoque
- clientes
- participantes/fornecedores
- contas a pagar
- contas a receber
- relatorios

## Requisitos
- Python 3.13 ou superior
- `pip`

Opcional:
- PostgreSQL, se voce quiser rodar com banco externo

## Como um usuario externo pode usar o sistema

### 1. Clonar o projeto
```bash
git clone <url-do-repositorio>
cd loja-roupa-py
```

### 2. Criar e ativar um ambiente virtual

Windows PowerShell:
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Windows CMD:
```bat
python -m venv venv
venv\Scripts\activate.bat
```

Linux/macOS:
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Instalar as dependencias
```bash
pip install -r requirements.txt
```

## Configuracao do banco

O projeto funciona de duas formas:

### Opcao A: uso local com SQLite
Nao precisa configurar nada.

Se a variavel `DATABASE_URL` nao existir, o sistema cria e usa automaticamente o arquivo local:

`dados/sistema_loja.db`

### Opcao B: uso com PostgreSQL
Defina a variavel de ambiente `DATABASE_URL` antes de iniciar a aplicacao.

Exemplo:
```bash
DATABASE_URL=postgresql://usuario:senha@host:5432/banco
```

No Windows PowerShell:
```powershell
$env:DATABASE_URL="postgresql://usuario:senha@host:5432/banco"
```

## Inicializacao do sistema

### 4. Criar as tabelas
```bash
python app/database/setup_db.py
```

### 5. Inserir dados iniciais de exemplo
```bash
python Tests/inserir_dados.py
```

Esse script pode ser executado mais de uma vez sem duplicar os registros principais.

## Executar a aplicacao

### 6. Rodar localmente
```bash
python run.py
```

Por padrao, a aplicacao sobe em ambiente local com debug habilitado.

Depois disso, acesse:

`http://127.0.0.1:5000`

## Fluxo recomendado para primeiro uso

Depois de abrir o sistema no navegador:

1. Acesse a tela inicial
2. Verifique se existem registros em Clientes e Participantes
3. Verifique se existe ao menos um produto em Estoque
4. Teste um lancamento em Vendas
5. Teste um lancamento em Compras
6. Consulte Contas a Pagar, Contas a Receber e Relatorios

Se voce executou `Tests/inserir_dados.py`, o sistema ja cria uma base minima para navegacao.

## Deploy

O projeto pode ser publicado em plataformas como Render.

Fluxo recomendado de deploy:

1. configurar a variavel `DATABASE_URL` no ambiente, se usar PostgreSQL
2. instalar dependencias com `pip install -r requirements.txt`
3. executar a criacao das tabelas:
   `python app/database/setup_db.py`
4. opcionalmente inserir dados iniciais:
   `python Tests/inserir_dados.py`
5. iniciar o servidor WSGI:
   `gunicorn run:app`

Comando de start completo:
```bash
python app/database/setup_db.py && python Tests/inserir_dados.py && gunicorn run:app
```

## Estrutura principal do projeto

```text
app/
  database/    acesso ao banco e repositories
  models/      entidades e validacoes
  routes/      blueprints e rotas da aplicacao
  services/    regras de negocio
  static/      css, js e imagens
  templates/   paginas HTML
Tests/
  inserir_dados.py
  test_post_routes.py
run.py
```

## Testes

Para rodar os testes principais de POST:
```bash
pytest Tests/test_post_routes.py -q -p no:cacheprovider
```

## Observacoes importantes

- O projeto usa nomes de arquivos sensiveis a maiusculas/minusculas em ambiente Linux.
- Em producao, nao exponha a `DATABASE_URL` em logs.
- Para ambiente local, o SQLite e suficiente para avaliacao e testes iniciais.

## Status atual

O projeto esta organizado em:
- blueprints para rotas
- service layer para regras de negocio
- repositories para persistencia
- suporte a SQLite e PostgreSQL
