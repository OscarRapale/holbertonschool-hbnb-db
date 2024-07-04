from src.models.user import User
from src.models.country import Country
from src.models.place import Place
from src.models.city import City
from src.persistence.repository import Repository
from src.persistence.db import DBRepository
from src import create_app

def main():
    app = create_app()
    with app.app_context():
        repo = DBRepository()
        populate_db(repo)

def populate_db(repo: Repository) -> None:
    """Populates the db with dummy users"""
    
    users = [
        User(first_name="Jane", last_name="Smith", password="password4", email="jane@example.com", is_admin=False),
        
    ]
    for user in users:
        repo.save(user)

    countries = [
        Country.create(name="New Zealand", code="NZ"),
    ]

    cities = [
        City(name="Wellington", country_code="NZ"),
    ]
    for city in cities:
        repo.save(city)

    places = [
        Place(name="Cozy Cottage", description="A cozy cottage in the countryside.", address="456 Country Lane", latitude=51.5074, longitude=0.1278, host_id=user.id, city_id=city.id,
                 price_per_night=100.0,  number_of_bathrooms=1, number_of_rooms=2,  max_guests=4)
    ]

    
    for country in countries:
        print(f"Country {country.name} saved.")
    
    
    for place in places:
        repo.save(place)

    print("DB populated")

if __name__ == "__main__":
    main()
