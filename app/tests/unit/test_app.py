from app.models import User


def test_new_user():
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email, hashed_password, and full_name
    """
    user = User('Archana Singh', 'archu04@gmail.com', 'FlaskIsAwesome', 'INR')
    assert user.email == 'archu04@gmail.com'
    assert user.full_name == 'Archana Singh'
    assert user.currency == 'INR'
