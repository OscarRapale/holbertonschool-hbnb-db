from src.models.base import Base
from src.models import db
from src.models.country import Country
from src.persistence.repository import Repository
from sqlalchemy.exc import SQLAlchemyError


class DBRepository(Repository):

    def __init__(self) -> None:
        self.__session = db.session
        self.reload()

    def get_all(self, model_name: str) -> list:
        try:
            return self.__session.query(model_name).all()
        except SQLAlchemyError:
            self.__session.rollback()
            return []

    def get(self, model_name: str, obj_id: str) -> Base | None:
        try:
            return self.__session.query(model_name).get(obj_id)
        except SQLAlchemyError:
            self.__session.rollback()
            return None

    def get_for_country(self, code: str) -> Base | None:
        try:
            return self.__session.query(Country).filter_by(code=code).first()
        except SQLAlchemyError:
            self.__session.rollback()
            return None
        

    def reload(self) -> None:
        self.__session = db.session
        

    def save(self, obj: Base) -> None:
        try:
            self.__session.add(obj)
            self.__session.commit()
        except SQLAlchemyError as e:
            self.__session.rollback()
            print(f"Error saving object: {SQLAlchemyError}")

    def update(self, obj: Base) -> None:
        try:
            self.__session.commit()
        except SQLAlchemyError:
            self.__session.rollback()

    def delete(self, obj: Base) -> bool:
        try:
            self.__session.delete(obj)
            self.__session.commit()
            return True
        except SQLAlchemyError:
            self.__session.rollback()
            return False

    def _get_model_class(self, model_name: str):
        """Helper method to get the model class by name"""
        from src.models.user import User
        from src.models.place import Place
        from src.models.review import Review
        from src.models.amenity import Amenity
        from src.models.city import City
        from src.models.country import Country

        models = {
            "user": User,
            "place": Place,
            "review": Review,
            "amenity": Amenity,
            "city": City,
            "country": Country,
        }

        return models[model_name.lower()]
