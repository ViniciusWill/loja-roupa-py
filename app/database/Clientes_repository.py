from app.models.Clientes_model import Cliente
from .base_repository import BaseRepository

class ClienteRepository(BaseRepository):
    def salvar(self, cliente):
        query = "INSERT INTO clientes (nome) VALUES (?)"
        query = query.replace("?", "%s") 
        self.executar_comando(query, (cliente.nome,))

    def buscar_todos(self):
        query = "SELECT * FROM clientes"
        rows = self.executar_select(query)
        return [{"id": row["id"], "nome": row["nome"]} for row in rows]

    def buscar_por_id(self, cliente_id):
        query = "SELECT * FROM clientes WHERE id = ?"
        query = query.replace("?", "%s") 
        rows = self.executar_select(query, (cliente_id,))
        return rows[0] if rows else None