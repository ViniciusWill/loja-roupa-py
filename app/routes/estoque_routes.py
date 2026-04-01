from flask import render_template, Blueprint
from app.database.estoque_repository import EstoqueRepository

estoque_bp = Blueprint("estoque", __name__)
@estoque_bp.route("/estoque")
def estoque():
        estoque_repo = EstoqueRepository()
        produtos = estoque_repo.buscar_todos()

        total_itens    = len(produtos)
        estoque_baixo  = sum(1 for p in produtos if 0 < p.quantidade <= 5)
        estoque_zerado = sum(1 for p in produtos if p.quantidade <= 0)

        return render_template(
            "Estoque/Estoque.html",
            logo_header="imagens/estoque.png",
            produtos=produtos,
            total_itens=total_itens,
            estoque_baixo=estoque_baixo,
            estoque_zerado=estoque_zerado,
        )