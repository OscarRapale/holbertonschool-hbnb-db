from src import db
from src.persistence.file import FileRepository
import os

class DataManager:
    def __init__(self):
        self.use_database = os.getenv('USE_DATABASE', 'False').lower() == 'true'
        if self.use_database:
            self.repo = None  # Use SQLAlchemy for database operations
        else:
            self.repo = FileRepository()

    def save(self, obj):
        if self.use_database:
            db.session.add(obj)
            db.session.commit()
        else:
            self.repo.save(obj)

    def delete(self, obj):
        if self.use_database:
            db.session.delete(obj)
            db.session.commit()
        else:
            self.repo.delete(obj)

    def load(self, cls, obj_id):
        if self.use_database:
            return cls.query.get(obj_id)
        else:
            return self.repo.get(cls.__name__.lower(), obj_id)

    def load_all(self, cls):
        if self.use_database:
            return cls.query.all()
        else:
            return self.repo.get_all(cls.__name__.lower())
