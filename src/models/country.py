"""
Country related functionality
"""
from . import db

class Country(db.Model):

    __tablename__ = 'countries'

    name = db.Column(db.String(128), nullable=False)
    code = db.Column(db.String(2), primary_key=True, nullable=False)
    cities = db.relationship("City", back_populates='country')


    def __init__(self, name: str, code: str, **kw) -> None:
        super().__init__(**kw)
        self.name = name
        self.code = code

    def __repr__(self) -> str:
        return f"<Country {self.code} ({self.name})>"

    def to_dict(self) -> dict:
        """Returns the dictionary representation of the country"""
        return {
            "name": self.name,
            "code": self.code,
        }

    @staticmethod
    def get_all() -> list["Country"]:
        """Get all countries"""
        from src.persistence import repo

        countries: list["Country"] = repo.get_all(Country)

        return countries

    @staticmethod
    def get(code: str) -> "Country | None":
        """Get a country by its code"""
        from src.persistence import repo

        country: "Country" = repo.get_for_country(code)

        return country

    @staticmethod
    def create(name: str, code: str) -> "Country":
        """Create a new country"""
        from src.persistence import repo
        
        country = Country(name, code)

        repo.save(country)

        return country
