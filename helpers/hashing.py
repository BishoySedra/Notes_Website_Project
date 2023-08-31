import bcrypt


def hash_password(password):
    salt_rounds = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt_rounds).decode()


def is_password_matched(password, stored_hashed_password):
    return bcrypt.checkpw(password.encode(), stored_hashed_password.encode())
