from src.models.user import User
from src.persistence.repository import Repository

def populate_db(repo: Repository) -> None:
    """Populates the db with dummy users"""
    
    users = [
        User(first_name="Test", last_name="User1", password="password2", email="test1@example.com", is_admin=False),
        User(first_name="Test", last_name="User2", password="password1", email="test2@example.com", is_admin=False),
        # Add more users as needed
    ]

    for user in users:
        repo.save(user)

    print("Memory DB populated with users")
