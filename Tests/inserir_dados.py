import psycopg2
import os
from datetime import datetime, timedelta

def popular_banco():
    DATABASE_URL = os.getenv('DATABASE_URL')
    
    if not DATABASE_URL:
        print("Erro: Variável DATABASE_URL não encontrada.")
        return

    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        print("Conectado ao banco para inserção...")

        # 1. Inserir Participantes (Fornecedores)
        cur.execute("INSERT INTO \"Participantes\" (nome) VALUES ('Fornecedor Alpha') RETURNING id")
        fornecedor_id = cur.fetchone()[0]

        # 2. Inserir Clientes
        cur.execute("INSERT INTO clientes (nome) VALUES ('João Silva') RETURNING id")
        cliente_id = cur.fetchone()[0]

        # 3. Inserir Estoque (Produtos)
        cur.execute("""
            INSERT INTO estoque (nome_produto, tamanho, quantidade, valor_compra) 
            VALUES ('Camiseta Polo', 'G', 50, 25.50) RETURNING id
        """)
        produto_id = cur.fetchone()[0]

        # 4. Inserir uma Compra
        cur.execute("""
            INSERT INTO compras (estoque_id, fornecedor_id, quantidade, valor_unitario, "Data_Compra") 
            VALUES (%s, %s, 10, 20.00, %s) RETURNING id
        """, (produto_id, fornecedor_id, datetime.now()))
        compra_id = cur.fetchone()[0]

        # 5. Inserir uma Conta a Pagar
        cur.execute("""
            INSERT INTO "Contas_a_pagar" (compra_id, parcela, valor_parcela, valor_pendente, data_vencimento) 
            VALUES (%s, 1, 200.00, 200.00, 20241231)
        """, (compra_id,))

        # 6. Inserir uma Venda
        cur.execute("""
            INSERT INTO vendas (cliente_id, estoque_id, quantidade, valor_unitario, data_venda) 
            VALUES (%s, %s, 2, 80.00, %s) RETURNING id
        """, (cliente_id, produto_id, datetime.now()))
        venda_id = cur.fetchone()[0]

        # 7. Inserir uma Conta a Receber
        cur.execute("""
            INSERT INTO "Contas_a_receber" (venda_id, parcela, valor_parcela, valor_pendente, data_vencimento) 
            VALUES (%s, 1, 160.00, 160.00, %s)
        """, (venda_id, datetime.now() + timedelta(days=30)))

        conn.commit()
        print("Dados fictícios inseridos com sucesso!")

    except Exception as e:
        print(f"Erro ao inserir dados: {e}")
    finally:
        if conn:
            cur.close()
            conn.close()

if __name__ == "__main__":
    popular_banco()