from src.models.user import User
from src.models.country import Country
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
        User(first_name="Test", last_name="User1", password="password2", email="test1@example.com", is_admin=False),
        User(first_name="Test", last_name="User2", password="password1", email="test2@example.com", is_admin=False),
        
    ]
    countries = [
        Country.create(name="Japan", code="JP", repo=repo),
    ]

    for user in users:
        repo.save(user)
    
    for country in countries:
        print(f"Country {country.name} saved.")


    print("DB populated")

if __name__ == "__main__":
    main()
