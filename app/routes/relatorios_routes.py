from flask import Blueprint, render_template

from app.database.Compras_repository import CompraRepository
from app.database.Vendas_repository import VendaRepository


relatorios_bp = Blueprint("relatorios", __name__)


@relatorios_bp.route("/relatorios")
def relatorios():
    compras_repo = CompraRepository()
    vendas_repo = VendaRepository()

    compras = compras_repo.selecionar_todas_compras()
    vendas = vendas_repo.selecionar_todas_vendas()

    total_compras = len(compras)
    total_vendas = len(vendas)
    faturamento_total = sum(venda.valor_unitario * venda.quantidade for venda in vendas)

    return render_template(
        "relatorios/Relatorios.html",
        logo_header="imagens/Relatorio.png",
        compras=compras,
        vendas=vendas,
        total_compras=total_compras,
        total_vendas=total_vendas,
        faturamento_total=faturamento_total,
    )
