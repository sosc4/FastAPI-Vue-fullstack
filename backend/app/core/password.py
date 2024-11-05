import re

from fastapi import HTTPException, status


def validate_password(password: str,
                      password_min_length: int,
                      password_require_digit: bool,
                      password_require_special: bool):
    if len(password) < password_min_length:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Hasło musi mieć co najmniej 12 znaków"
        )

    if password_require_digit and not re.search(r"\d", password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Hasło musi zawierać co najmniej jedną cyfrę"
        )

    if password_require_special and not re.search(r"[!@#$%^&*()_\-+=\[\]{};:'\"|\\,.<>?/~`]", password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Hasło musi zawierać co najmniej jeden znak specjalny"
        )
