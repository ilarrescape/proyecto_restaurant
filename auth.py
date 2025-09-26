"""Utilities for secure user authentication."""
from __future__ import annotations

import argparse
import base64
import os
import sqlite3
import sys
from contextlib import contextmanager
from pathlib import Path
import hashlib
import hmac
from typing import Iterable, Tuple

_DB_PATH = Path(__file__).resolve().parent / "recetas.db"
_PBKDF2_ITERATIONS = 200_000
_SALT_BYTES = 16


def _get_connection() -> sqlite3.Connection:
    """Return a SQLite connection to the project database."""
    return sqlite3.connect(_DB_PATH)


@contextmanager
def db_cursor() -> Iterable[sqlite3.Cursor]:
    """Context manager that yields a database cursor and commits on success."""
    connection = _get_connection()
    cursor = connection.cursor()
    try:
        yield cursor
        connection.commit()
    finally:
        cursor.close()
        connection.close()


def initialize_user_table() -> None:
    """Create the user table if it does not exist."""
    with db_cursor() as cursor:
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS usuario (
                id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre_usuario TEXT UNIQUE NOT NULL,
                hash_contrasena TEXT NOT NULL,
                sal_contrasena TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )


def _hash_password(password: str, salt: bytes | None = None) -> Tuple[str, str]:
    """Generate a PBKDF2 hash for the provided password."""
    if not isinstance(password, str) or not password:
        raise ValueError("La contraseña debe ser una cadena no vacía.")

    salt_bytes = salt if salt is not None else os.urandom(_SALT_BYTES)
    derived_key = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt_bytes,
        _PBKDF2_ITERATIONS,
    )
    return base64.b64encode(salt_bytes).decode("utf-8"), base64.b64encode(derived_key).decode("utf-8")


def create_user(username: str, password: str, *, overwrite: bool = False) -> None:
    """Create a new user with a securely hashed password."""
    if not isinstance(username, str) or not username:
        raise ValueError("El nombre de usuario debe ser una cadena no vacía.")

    initialize_user_table()
    salt_b64, hash_b64 = _hash_password(password)

    with db_cursor() as cursor:
        cursor.execute(
            "SELECT id_usuario FROM usuario WHERE nombre_usuario = ?",
            (username,),
        )
        existing = cursor.fetchone()
        if existing and not overwrite:
            raise ValueError("El usuario ya existe. Use --overwrite para reemplazarlo.")
        if existing and overwrite:
            cursor.execute(
                "UPDATE usuario SET hash_contrasena = ?, sal_contrasena = ? WHERE nombre_usuario = ?",
                (hash_b64, salt_b64, username),
            )
        else:
            cursor.execute(
                "INSERT INTO usuario (nombre_usuario, hash_contrasena, sal_contrasena) VALUES (?, ?, ?)",
                (username, hash_b64, salt_b64),
            )


def verify_user(username: str, password: str) -> bool:
    """Return True if the provided credentials match a stored user."""
    initialize_user_table()
    with db_cursor() as cursor:
        cursor.execute(
            "SELECT hash_contrasena, sal_contrasena FROM usuario WHERE nombre_usuario = ?",
            (username,),
        )
        row = cursor.fetchone()
    if row is None:
        return False

    stored_hash_b64, salt_b64 = row
    salt = base64.b64decode(salt_b64.encode("utf-8"))
    _, computed_hash_b64 = _hash_password(password, salt=salt)
    return hmac.compare_digest(stored_hash_b64, computed_hash_b64)


def _parse_args(argv: Iterable[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Gestión de usuarios para la aplicación de recetas.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    create_parser = subparsers.add_parser("crear-usuario", help="Crear o actualizar un usuario")
    create_parser.add_argument("usuario", help="Nombre de usuario a crear")
    create_parser.add_argument("contraseña", help="Contraseña para el usuario")
    create_parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Sobrescribe la contraseña si el usuario ya existe.",
    )

    return parser.parse_args(argv)


def main(argv: Iterable[str] | None = None) -> int:
    args = _parse_args(argv or sys.argv[1:])
    if args.command == "crear-usuario":
        try:
            create_user(args.usuario, args.contraseña, overwrite=args.overwrite)
            print(f"Usuario '{args.usuario}' creado/actualizado correctamente.")
            return 0
        except ValueError as exc:  # pragma: no cover - user input validation
            print(exc, file=sys.stderr)
            return 1
    raise ValueError("Comando desconocido")


if __name__ == "__main__":
    sys.exit(main())
