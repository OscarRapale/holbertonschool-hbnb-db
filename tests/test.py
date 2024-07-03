from src import create_app
from src.models import db
from src.models.country import Country

app = create_app()

with app.app_context():
    # Create a new country
    new_country = Country(name='Puerto Rico', code='PR')
    db.session.add(new_country)
    db.session.commit()

    # Read the country
    country = Country.query.filter_by(name='Puerto Rico').first()
    assert country is not None, "Country was not created"
    assert country.name == 'Puerto Rico', "Country name does not match"
    assert country.code == 'PR', "Country code does not match"

    # Update the country
    #country.name = 'USA'
    #db.session.commit()

    # Verify the update
    #updated_country = Country.query.filter_by(code='US').first()
    #assert updated_country.name == 'USA', "Country was not updated"

    # Delete the country
    db.session.delete(country)
    db.session.commit()

    # Verify the delete
    deleted_country = Country.query.filter_by(code='PR').first()
    assert deleted_country is None, "Country was not deleted"
