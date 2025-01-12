import math
from dataclasses import dataclass

import bcrypt
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@dataclass
class SolveBugBcryptWarning:
    __version__: str = getattr(bcrypt, "__version__")


setattr(bcrypt, "__about__", SolveBugBcryptWarning())


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def validate_otp(otp: str = None, x: int = None, a: int = None) -> bool:
    try:
        otp = float(otp)

    except ValueError:
        return False

    if not all(x is not None for x in [otp, x, a]):
        return False

    try:
        if a * x < 0:
            return False

        if not round(otp, 3) == otp:
            return False

        calculated_value = math.log10(a * x)

        calculated_otp = round(calculated_value, 3)

        return calculated_otp == otp

    except (ValueError, OverflowError):
        return False


if __name__ == '__main__':
    print(
        math.log10(1)
    )
