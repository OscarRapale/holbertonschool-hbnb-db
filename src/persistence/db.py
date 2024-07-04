from src.models.base import Base
from src.models import db
from src.models.country import Country
from src.persistence.repository import Repository
from sqlalchemy.exc import SQLAlchemyError


class DBRepository(Repository):
    """
    DBRepository class to handle database operations.

    This class provides an interface for getting all instances of a model, getting a specific instance by ID,
    getting a country by code, saving, updating, and deleting instances, and reloading the session.
    It inherits from the Repository class and overrides its methods to use SQLAlchemy for database operations.
    """

    def __init__(self) -> None:
        """
        Initialize DBRepository instance.

        This method sets the session to the current database session and reloads the session.
        """
        self.__session = db.session
        self.reload()

    def get_all(self, model_name: str) -> list:
        """
        Get all instances of a model.

        Args:
            model_name: The name of the model to get instances of.

        Returns:
            A list of all instances of the model, or an empty list if an error occurred.
        """
        try:
            return self.__session.query(model_name).all()
        except SQLAlchemyError:
            self.__session.rollback()
            return []

    def get(self, model_name: str, obj_id: str) -> Base | None:
        """
        Get a specific instance of a model by ID.

        Args:
            model_name: The name of the model to get an instance of.
            obj_id: The ID of the instance to get.

        Returns:
            The instance with the given ID, or None if no such instance exists or an error occurred.
        """
        try:
            return self.__session.query(model_name).get(obj_id)
        except SQLAlchemyError:
            self.__session.rollback()
            return None

    def get_for_country(self, code: str) -> Base | None:
        """
        Get a country by code.

        Args:
            code: The code of the country to get.

        Returns:
            The country with the given code, or None if no such country exists or an error occurred.
        """
        try:
            return self.__session.query(Country).filter_by(code=code).first()
        except SQLAlchemyError:
            self.__session.rollback()
            return None

    def reload(self) -> None:
        """
        Reload the session.

        This method sets the session to the current database session.
        """
        self.__session = db.session

    def save(self, obj: Base) -> None:
        """
        Save an instance.

        Args:
            obj: The instance to save.
        """
        try:
            self.__session.add(obj)
            self.__session.commit()
        except SQLAlchemyError as e:
            self.__session.rollback()
            print(f"Error saving object: {SQLAlchemyError}")

    def update(self, obj: Base) -> None:
        """
        Update an instance.

        Args:
            obj: The instance to update.
        """
        try:
            self.__session.commit()
        except SQLAlchemyError:
            self.__session.rollback()

    def delete(self, obj: Base) -> bool:
        """
        Delete an instance.

        Args:
            obj: The instance to delete.

        Returns:
            True if the instance was deleted successfully, or False if an error occurred.
        """
        try:
            self.__session.delete(obj)
            self.__session.commit()
            return True
        except SQLAlchemyError:
            self.__session.rollback()
            return False

    def _get_model_class(self, model_name: str):
        """
        Get the model class by name.

        Args:
            model_name: The name of the model class to get.

        Returns:
            The model class with the given name, or None if no such class exists.

        This is a helper method used internally by the DBRepository class.
        """
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
