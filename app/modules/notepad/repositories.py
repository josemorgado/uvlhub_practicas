from app.modules.notepad.models import Notepad
from core.repositories.BaseRepository import BaseRepository


class NotepadRepository(BaseRepository):
    def __init__(self):
        super().__init__(Notepad)

    def get_all_by_user(self, user_id):
        # Pide los notepads del usuario a la base de datos
        return Notepad.query.filter_by(user_id=user_id).all()

    def create(self, title, body, user_id):
        notepad = Notepad(
            title=title,
            body=body,
            user_id=user_id
        )
        self.session.add(notepad)
        self.session.commit()
        return notepad