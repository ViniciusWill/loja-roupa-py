from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.database.Participantes_repository import ParticipantesRepository
from app.services.participantes_service import ParticipanteService


participantes_bp = Blueprint("participantes", __name__)


@participantes_bp.route("/participantes", methods=["GET", "POST"])
def participantes():
    if request.method == "POST":
        try:
            nome = request.form.get("nome", "").strip()
            ParticipanteService().lancamento_participante(nome=nome)
            flash("Participante cadastrado com sucesso!", "sucesso")
            return redirect(url_for("participantes.participantes"))
        except Exception as exc:
            flash(f"Erro ao cadastrar participante: {exc}", "erro")

    participantes_repo = ParticipantesRepository()
    partic = participantes_repo.buscar_todos()
    total_partic = len(partic)
    return render_template(
        "participantes/Participantes.html",
        logo_header="imagens/participantes.png",
        partic=partic,
        total_partic=total_partic,
    )
