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
    from src.models.amenity import PlaceAmenity
    from src.models.review import Review

    user = User(email="oscarrapale@example.com", password="password123", first_name="Oscar", last_name="Rapale", is_admin=True)
    db.session.add(user)

    db.session.add(Country(name="Puerto Rico", code="PR"))

    city = City(name="Miami", country_code="US")
    db.session.add(city)

    #place = Place(name="My Awesome Place", description="An awesome place.", address="123 Main street", latitude=40.7826, longitude=73.9656, host_id=user.id, city_id=city.id,
                 #price_per_night=150.0,  number_of_bathrooms=1, number_of_rooms=2,  max_guests=3)
    #db.session.add(place)

    db.session.commit()
    print("Database seeded.")


if __name__ == "__main__":
    cli()
