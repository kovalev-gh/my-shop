import bcrypt


def hash_password(
    password: str,
) -> str:

    salt = bcrypt.gensalt()

    hashed_password = bcrypt.hashpw(
        password.encode(),
        salt,
    )

    return hashed_password.decode()


def validate_password(
    password: str,
    hashed_password: str,
) -> bool:

    return bcrypt.checkpw(
        password=password.encode(),
        hashed_password=hashed_password.encode(),
    )