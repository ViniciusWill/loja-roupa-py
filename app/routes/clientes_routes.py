from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.database.Clientes_repository import ClienteRepository
from app.services.clientes_service import ClienteService


clientes_bp = Blueprint("clientes", __name__)


@clientes_bp.route("/clientes", methods=["GET", "POST"])
def clientes():
    if request.method == "POST":
        try:
            nome = request.form.get("nome", "").strip()
            ClienteService().lancamento_cliente(nome=nome)
            flash("Cliente cadastrado com sucesso!", "sucesso")
            return redirect(url_for("clientes.clientes"))
        except Exception as exc:
            flash(f"Erro ao cadastrar cliente: {exc}", "erro")

    clientes_repo = ClienteRepository()
    cli = clientes_repo.buscar_todos()
    total_cli = len(cli)
    return render_template(
        "clientes/Clientes.html",
        logo_header="imagens/Clientes.png",
        cli=cli,
        total_cli=total_cli,
    )
