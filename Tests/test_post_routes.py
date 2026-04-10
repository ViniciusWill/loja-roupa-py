import sqlite3
import sys
import uuid
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app import create_app
from app.database.base_repository import BaseRepository


SCHEMA = [
    """
    CREATE TABLE clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL UNIQUE
    )
    """,
    """
    CREATE TABLE estoque (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome_produto TEXT NOT NULL,
        tamanho TEXT NOT NULL,
        quantidade INTEGER NOT NULL,
        valor_compra REAL NOT NULL,
        UNIQUE(nome_produto, tamanho)
    )
    """,
    """
    CREATE TABLE Participantes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL UNIQUE
    )
    """,
    """
    CREATE TABLE compras (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        estoque_id INTEGER NOT NULL,
        fornecedor_id INTEGER NOT NULL,
        quantidade INTEGER NOT NULL,
        valor_unitario REAL NOT NULL,
        data_compra TEXT NOT NULL
    )
    """,
    """
    CREATE TABLE vendas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente_id INTEGER NOT NULL,
        estoque_id INTEGER NOT NULL,
        quantidade INTEGER NOT NULL,
        valor_unitario REAL NOT NULL,
        data_venda TEXT NOT NULL
    )
    """,
    """
    CREATE TABLE contas_a_pagar (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        compra_id INTEGER NOT NULL,
        parcela INTEGER NOT NULL,
        valor_parcela REAL NOT NULL,
        valor_pendente REAL NOT NULL,
        data_vencimento TEXT NOT NULL
    )
    """,
    """
    CREATE TABLE contas_a_receber (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        venda_id INTEGER NOT NULL,
        parcela INTEGER NOT NULL,
        valor_parcela REAL NOT NULL,
        valor_pendente REAL NOT NULL,
        data_vencimento TEXT NOT NULL
    )
    """,
]


@pytest.fixture()
def client(monkeypatch):
    temp_dir = Path("Tests") / ".tmp"
    temp_dir.mkdir(exist_ok=True)
    db_path = temp_dir / f"test_loja_{uuid.uuid4().hex}.db"

    def fake_init(self):
        self.db_url = None
        self.is_postgres = False
        self.caminho_banco = Path(db_path)

    monkeypatch.setattr(BaseRepository, "__init__", fake_init)

    conn = sqlite3.connect(db_path)
    try:
        for statement in SCHEMA:
            conn.execute(statement)

        conn.execute("INSERT INTO clientes (nome) VALUES (?)", ("Cliente Base",))
        conn.execute(
            "INSERT INTO estoque (nome_produto, tamanho, quantidade, valor_compra) VALUES (?, ?, ?, ?)",
            ("Camiseta Polo", "G", 10, 25.50),
        )
        conn.execute("INSERT INTO Participantes (nome) VALUES (?)", ("Fornecedor Base",))
        conn.commit()
    finally:
        conn.close()

    app = create_app()
    app.config.update(TESTING=True)

    try:
        with app.test_client() as test_client:
            yield test_client, db_path
    finally:
        if db_path.exists():
            db_path.unlink()


def fetch_one(db_path, query, params=()):
    conn = sqlite3.connect(db_path)
    try:
        return conn.execute(query, params).fetchone()
    finally:
        conn.close()


def test_post_vendas_persiste_registro_e_atualiza_estoque(client):
    test_client, db_path = client

    response = test_client.post(
        "/vendas",
        data={"cliente_id": "1", "estoque_id": "1", "Quantidade-ven": "2", "parcelas": "1"},
        follow_redirects=False,
    )

    assert response.status_code == 302
    venda = fetch_one(db_path, "SELECT quantidade, valor_unitario FROM vendas")
    estoque = fetch_one(db_path, "SELECT quantidade FROM estoque WHERE id = 1")
    assert venda == (2, 25.5)
    assert estoque == (8,)


def test_post_compras_persiste_registro_e_atualiza_estoque(client):
    test_client, db_path = client

    response = test_client.post(
        "/compras",
        data={"fornecedor_id": "1", "estoque_id": "1", "quantidade": "3", "parcelas": "1"},
        follow_redirects=False,
    )

    assert response.status_code == 302
    compra = fetch_one(db_path, "SELECT quantidade, valor_unitario FROM compras")
    estoque = fetch_one(db_path, "SELECT quantidade FROM estoque WHERE id = 1")
    assert compra == (3, 25.5)
    assert estoque == (13,)


def test_post_clientes_persiste_registro(client):
    test_client, db_path = client

    response = test_client.post(
        "/clientes",
        data={"nome": "Cliente Novo"},
        follow_redirects=False,
    )

    assert response.status_code == 302
    cliente = fetch_one(db_path, "SELECT nome FROM clientes WHERE nome = ?", ("Cliente Novo",))
    assert cliente == ("Cliente Novo",)


def test_post_participantes_persiste_registro(client):
    test_client, db_path = client

    response = test_client.post(
        "/participantes",
        data={"nome": "Fornecedor Novo"},
        follow_redirects=False,
    )

    assert response.status_code == 302
    participante = fetch_one(
        db_path,
        "SELECT nome FROM Participantes WHERE nome = ?",
        ("Fornecedor Novo",),
    )
    assert participante == ("Fornecedor Novo",)
