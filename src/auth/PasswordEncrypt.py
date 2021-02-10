import bcrypt


def encrypt(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf8'), salt)
    return hashed


def decrypt(password, hashed_pswr):
    if bcrypt.checkpw(password.encode('utf8'), hashed_pswr):
        return True
    else:
        return False
