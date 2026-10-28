from app.core.security import hash_password, verify_password


def test_password_is_hashed():
    password = "Password@123"

    hashed_password = hash_password(password)

    assert hashed_password != password


def test_verify_correct_password():
    password = "Password@123"
    hashed_password = hash_password(password)

    assert verify_password(password, hashed_password) == True


def test_verify_incorrect_password():
    password = "Password@123"
    hashed_password = hash_password(password)

    assert verify_password("mike@123", hashed_password) == False

    # python -m pytest tests/test_security.py -v


    