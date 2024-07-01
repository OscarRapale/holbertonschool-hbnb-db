from src import create_app
from src.models import db
from src.models.user import User

app = create_app()

with app.app_context():
    # Create a new user
    new_user = User(email='testing@example.com', password='securepassword', first_name='Test', last_name='User', is_admin=False)
    db.session.add(new_user)
    db.session.commit()

    # Read the user
    user = User.query.filter_by(email='testing@example.com').first()
    assert user is not None, "User was not created"
    assert user.email == 'testing@example.com', "User email does not match"
    assert user.first_name == 'Test', "User first name does not match"
    assert user.last_name == 'User', "User last name does not match"
    assert user.is_admin == False, "User is_admin does not match"

    # Update the user
    user.first_name = 'Updated'
    db.session.commit()

    # Verify the update
    updated_user = User.query.filter_by(email='testing@example.com').first()
    assert updated_user.first_name == 'Updated', "User was not updated"

    # Delete the user
    db.session.delete(user)
    db.session.commit()

    # Verify the delete
    deleted_user = User.query.filter_by(email='testing@example.com').first()
    assert deleted_user is None, "User was not deleted"
