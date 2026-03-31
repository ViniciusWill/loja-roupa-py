from flask import render_template, Blueprint
from app.database.Vendas_repository import VendaRepository
from datetime import datetime

contas_a_receber_bp = Blueprint("contas_a_receber", __name__)

@contas_a_receber_bp.route("/financeiro/contas_receber")
def contas_receber():
        repo = VendaRepository()
        contas = repo.buscar_todos_areceber()
        hoje   = datetime.now()

        for c in contas:
            if c.data_vencimento.tzinfo is not None:
                c.data_vencimento = c.data_vencimento.replace(tzinfo=None)
 
        total_contas   = len(contas)
        total_pendente = sum(c.valor_pendente for c in contas if c.valor_pendente > 0)
        total_vencidas = sum(1 for c in contas if c.valor_pendente > 0 and c.data_vencimento < hoje)
 
        return render_template(
        "Financeiro/ContasReceber.html",
        logo_header="imagens/receber.png",
        contas=contas,
        hoje=hoje,
        total_contas=total_contas,
        total_pendente=total_pendente,
        total_vencidas=total_vencidas,
    )