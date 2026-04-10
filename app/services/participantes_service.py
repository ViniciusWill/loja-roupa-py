from app.database.Participantes_repository import ParticipantesRepository
from app.models.Participantes_model import Participante


class ParticipanteService:
    def __init__(self):
        self.participante_repo = ParticipantesRepository()

    def lancamento_participante(self, nome: str):
        novo_participante = Participante(nome=nome)
        self.participante_repo.lancamento_participante(novo_participante)
