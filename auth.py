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

from cryptography.fernet import Fernet, InvalidToken

_DB_PATH = Path(__file__).resolve().parent / "recetas.db"
_KEY_PATH = Path(__file__).resolve().parent / "auth_key.key"
_PBKDF2_ITERATIONS = 200_000
_SALT_BYTES = 16


def _get_connection() -> sqlite3.Connection:
    """Return a SQLite connection to the project database."""
    return sqlite3.connect(_DB_PATH)


def _load_or_create_key() -> bytes:
    """Return a Fernet key, creating it if necessary."""
    if _KEY_PATH.exists():
        return _KEY_PATH.read_bytes()

    key = Fernet.generate_key()
    _KEY_PATH.write_bytes(key)
    try:
        os.chmod(_KEY_PATH, 0o600)
    except OSError:
        # Best-effort permissions hardening; ignore on unsupported platforms.
        pass
    return key


def _get_cipher() -> Fernet:
    """Instantiate and return the Fernet cipher used for usernames."""
    return Fernet(_load_or_create_key())


def _hash_username(username: str) -> str:
    """Derive a deterministic hash for username lookups."""
    if not isinstance(username, str) or not username:
        raise ValueError("El nombre de usuario debe ser una cadena no vacía.")
    return hashlib.sha256(username.encode("utf-8")).hexdigest()


def _encrypt_username(username: str) -> str:
    """Encrypt the provided username for storage."""
    cipher = _get_cipher()
    token = cipher.encrypt(username.encode("utf-8"))
    return token.decode("utf-8")


def _decrypt_username(token: str) -> str:
    """Decrypt an encrypted username token."""
    cipher = _get_cipher()
    try:
        return cipher.decrypt(token.encode("utf-8")).decode("utf-8")
    except InvalidToken:  # pragma: no cover - defensive branch
        return ""


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
                nombre_usuario_hash TEXT UNIQUE NOT NULL,
                nombre_usuario_cifrado TEXT NOT NULL,
                hash_contrasena TEXT NOT NULL,
                sal_contrasena TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

    _ensure_user_table_schema()


def _ensure_user_table_schema() -> None:
    """Upgrade legacy schemas to include hashed and encrypted usernames."""
    with db_cursor() as cursor:
        cursor.execute("PRAGMA table_info(usuario)")
        columns = {row[1] for row in cursor.fetchall()}
        if not columns:
            return

        if {"nombre_usuario_hash", "nombre_usuario_cifrado"}.issubset(columns):
            return

        if "nombre_usuario" not in columns:
            raise RuntimeError(
                "Esquema de tabla 'usuario' inesperado; se requiere intervención manual."
            )

        cipher = _get_cipher()

        cursor.execute("ALTER TABLE usuario RENAME TO usuario_legacy")
        cursor.execute(
            """
            CREATE TABLE usuario (
                id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre_usuario_hash TEXT UNIQUE NOT NULL,
                nombre_usuario_cifrado TEXT NOT NULL,
                hash_contrasena TEXT NOT NULL,
                sal_contrasena TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        cursor.execute(
            "SELECT id_usuario, nombre_usuario, hash_contrasena, sal_contrasena, created_at FROM usuario_legacy"
        )
        rows = cursor.fetchall()
        for user_id, username, hash_pw, salt, created_at in rows:
            username_hash = hashlib.sha256(username.encode("utf-8")).hexdigest()
            encrypted_username = cipher.encrypt(username.encode("utf-8")).decode("utf-8")
            cursor.execute(
                """
                INSERT INTO usuario (
                    id_usuario,
                    nombre_usuario_hash,
                    nombre_usuario_cifrado,
                    hash_contrasena,
                    sal_contrasena,
                    created_at
                ) VALUES (?, ?, ?, ?, ?, ?)
                """,
                (user_id, username_hash, encrypted_username, hash_pw, salt, created_at),
            )

        cursor.execute("DROP TABLE usuario_legacy")


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
    initialize_user_table()
    username_hash = _hash_username(username)
    encrypted_username = _encrypt_username(username)
    salt_b64, hash_b64 = _hash_password(password)

    with db_cursor() as cursor:
        cursor.execute(
            "SELECT id_usuario FROM usuario WHERE nombre_usuario_hash = ?",
            (username_hash,),
        )
        existing = cursor.fetchone()
        if existing and not overwrite:
            raise ValueError("El usuario ya existe. Use --overwrite para reemplazarlo.")
        if existing and overwrite:
            cursor.execute(
                """
                UPDATE usuario
                   SET hash_contrasena = ?,
                       sal_contrasena = ?,
                       nombre_usuario_cifrado = ?
                 WHERE nombre_usuario_hash = ?
                """,
                (hash_b64, salt_b64, encrypted_username, username_hash),
            )
        else:
            cursor.execute(
                """
                INSERT INTO usuario (
                    nombre_usuario_hash,
                    nombre_usuario_cifrado,
                    hash_contrasena,
                    sal_contrasena
                ) VALUES (?, ?, ?, ?)
                """,
                (username_hash, encrypted_username, hash_b64, salt_b64),
            )


def verify_user(username: str, password: str) -> str | None:
    """Return the stored username when the credentials are valid."""
    initialize_user_table()
    username_hash = _hash_username(username)
    with db_cursor() as cursor:
        cursor.execute(
            """
            SELECT hash_contrasena, sal_contrasena, nombre_usuario_cifrado
              FROM usuario
             WHERE nombre_usuario_hash = ?
            """,
            (username_hash,),
        )
        row = cursor.fetchone()
    if row is None:
        return None

    stored_hash_b64, salt_b64, encrypted_username = row
    salt = base64.b64decode(salt_b64.encode("utf-8"))
    _, computed_hash_b64 = _hash_password(password, salt=salt)
    if not hmac.compare_digest(stored_hash_b64, computed_hash_b64):
        return None

    decrypted = _decrypt_username(encrypted_username)
    return decrypted or username


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
