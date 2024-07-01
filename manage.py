from flask.cli import FlaskGroup
from src import create_app
from src.models import db

app = create_app()

cli = FlaskGroup(create_app=create_app)


@cli.command("create_db")
def create_db():
    """Initialize the database."""
    db.create_all()
    print("Database created.")


@cli.command("drop_db")
def drop_db():
    """Drop the database."""
    db.drop_all()
    print("Database dropped.")


@cli.command("seed_db")
def seed_db():
    """Seed the database with initial data."""
    from src.models.user import User
    from src.models.country import Country
    from src.models.city import City
    from src.models.place import Place
    from src.models.amenity import Amenity
    from src.models.review import Review

    db.session.add(User(email="admin@example.com", first_name="Admin", last_name="User"))
    db.session.add(Country(name="United States", code="US"))
    # Add more initial data here...
    db.session.commit()
    print("Database seeded.")


if __name__ == "__main__":
    cli()
