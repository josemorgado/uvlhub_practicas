from app.modules.notepad.repositories import NotepadRepository
from core.services.BaseService import BaseService


class NotepadService(BaseService):
    def __init__(self):
        super().__init__(NotepadRepository())

    def get_all_by_user(self, user_id):
        # Pide los notepads al repositorio
        return self.repository.get_all_by_user(user_id)

    def create(self, title, body, user_id):
        # Crea un notepad en la base de datos
        return self.repository.create(title, body, user_id)
