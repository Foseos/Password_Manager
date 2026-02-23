"""
models/database.py

RÔLE (Model) : Toute interaction avec la base de données SQLite.
Pas de logique métier ici, uniquement du stockage/récupération de données.

BIBLIOTHÈQUE : sqlite3 (incluse dans Python, pas besoin d'installer)

════════════════════════════════════════════════════════════════
CONCEPTS À CONNAÎTRE
════════════════════════════════════════════════════════════════

1. CONNEXION
    import sqlite3
    conn = sqlite3.connect("passwords.db")  # crée le fichier si inexistant
    conn.row_factory = sqlite3.Row          # permet d'accéder aux colonnes par nom
    cursor = conn.cursor()

2. CRÉATION DE TABLE (CREATE TABLE IF NOT EXISTS)
    cursor.execute("
        CREATE TABLE IF NOT EXISTS passwords (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            service     TEXT NOT NULL,
            ...
        )
    ")
    conn.commit()

3. INSERTION (INSERT INTO)
    cursor.execute(
        "INSERT INTO passwords (service, username, password) VALUES (?, ?, ?)",
        (service, username, password)   # ← paramètres liés, jamais de f-string !
    )
    conn.commit()

4. LECTURE (SELECT)
    rows = cursor.execute("SELECT * FROM passwords").fetchall()
    for row in rows:
        print(row["service"])   # accès par nom grâce à row_factory

5. MISE À JOUR (UPDATE)
    cursor.execute(
        "UPDATE passwords SET service=? WHERE id=?",
        (new_service, pid)
    )
    conn.commit()

6. SUPPRESSION (DELETE)
    cursor.execute("DELETE FROM passwords WHERE id=?", (pid,))
    conn.commit()

════════════════════════════════════════════════════════════════
SCHÉMA DES TABLES À CRÉER
════════════════════════════════════════════════════════════════

TABLE master
    id      INTEGER PRIMARY KEY
    hash    TEXT NOT NULL          ← hash PBKDF2 du mot de passe maître
    salt    BLOB NOT NULL          ← sel utilisé pour le hash

TABLE passwords
    id          INTEGER PRIMARY KEY AUTOINCREMENT
    service     TEXT NOT NULL      ← ex: "GitHub", "Gmail"
    username    TEXT NOT NULL      ← email ou login
    password    TEXT NOT NULL      ← mot de passe CHIFFRÉ (jamais en clair)
    url         TEXT               ← optionnel
    notes       TEXT               ← optionnel
    created_at  TEXT DEFAULT (datetime('now','localtime'))
    updated_at  TEXT DEFAULT (datetime('now','localtime'))

════════════════════════════════════════════════════════════════
CONSEIL : utilise un context manager `with conn:` pour auto-commit/rollback
════════════════════════════════════════════════════════════════

À TOI DE JOUER — Implémente les fonctions ci-dessous
"""

import sqlite3
import hashlib
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "passwords.db"


def get_connection() -> sqlite3.Connection:
    """Retourne une connexion SQLite avec row_factory activé."""

    conn = sqlite3.connect("passwords.db")  # crée le fichier si inexistant
    conn.row_factory = sqlite3.Row          # permet d'accéder aux colonnes par nom
    cursor = conn.cursor()
    return conn


def init_db():
    """Crée les tables master et passwords si elles n'existent pas encore."""
    # TODO: avec get_connection(), execute CREATE TABLE IF NOT EXISTS pour
    #       les deux tables décrites ci-dessus (utilise executescript pour
    #       exécuter plusieurs requêtes d'un coup)

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS master (
            id          INTEGER PRIMARY KEY,
            hash        TEXT NOT NULL,
            salt        BLOB NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS passwords (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            service     TEXT NOT NULL,
            username    TEXT NOT NULL,
            password    TEXT NOT NULL,
            url         TEXT,
            notes       TEXT,
            created_at  TEXT DEFAULT (datetime('now','localtime')),
            updated_at  TEXT DEFAULT (datetime('now','localtime'))
        )
    """)

    conn.commit()
    conn.close()

# ── Mot de passe maître ────────────────────────────────────────────────────────

def master_exists() -> bool:
    """Retourne True si un mot de passe maître a déjà été créé."""
    # TODO: SELECT COUNT(*) FROM master — retourne row[0] > 0
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM master")
    result = cursor.fetchone()
    conn.close()
    return result[0] > 0


def save_master(password: str, salt: bytes):
    """
    Hash le mot de passe avec PBKDF2-SHA256 et le stocke avec son sel.
    Hint: hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 480_000)
    Stocke le hash en hexadécimal (.hex()) et le sel en BLOB.
    """
    # TODO: calcule le hash, supprime l'ancien enregistrement (DELETE FROM master)
    #       puis INSERT INTO master (hash, salt)


    hash = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 480_000).hex()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM master")
    cursor.execute("INSERT INTO master (hash, salt) VALUES (?, ?)", (hash, salt))

    conn.commit()
    conn.close()


def verify_master(password: str) -> tuple[bool, bytes]:
    """
    Vérifie le mot de passe maître.
    Retourne (True, salt) si correct, (False, b"") sinon.
    """
    # TODO: récupère hash + salt depuis la table master
    #       recalcule le hash avec le salt récupéré
    #       compare avec == et retourne le tuple approprié

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT hash, salt FROM master")
    result = cursor.fetchone()
    conn.close()
    if result:
        hash, salt = result
        return hash == hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 480_000).hex(), salt
    return False, b""


def get_master_salt() -> bytes:
    """Retourne le sel du mot de passe maître."""
    # TODO: SELECT salt FROM master

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT salt FROM master")
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else b""
    


# ── CRUD mots de passe ─────────────────────────────────────────────────────────

def add_password(service: str, username: str, password: str,
                 url: str = "", notes: str = "") -> int:
    """Insère une nouvelle entrée et retourne son id."""
    # TODO: INSERT INTO passwords ... retourne cursor.lastrowid

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO passwords (service, username, password, url, notes) VALUES (?, ?, ?, ?, ?)", (service, username, password, url, notes))
    new_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return new_id


def get_all_passwords() -> list:
    """Retourne toutes les entrées triées par service (insensible à la casse)."""
    # TODO: SELECT * FROM passwords ORDER BY service COLLATE NOCASE

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM passwords ORDER BY service COLLATE NOCASE")
    result = cursor.fetchall()
    conn.close()
    return result


def search_passwords(query: str) -> list:
    """Retourne les entrées dont service ou username contient query."""
    # TODO: SELECT * WHERE service LIKE ? OR username LIKE ?
    #       avec q = f"%{query}%"

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM passwords WHERE service LIKE ? OR username LIKE ?", (f"%{query}%", f"%{query}%"))
    result = cursor.fetchall()
    conn.close()
    return result


def get_password_by_id(pid: int):
    """Retourne une entrée par son id (ou None si inexistant)."""
    # TODO: SELECT * FROM passwords WHERE id = ?  → .fetchone()

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM passwords WHERE id = ?", (pid,))
    result = cursor.fetchone()
    conn.close()
    return result


def update_password(pid: int, service: str, username: str, password: str,
                    url: str = "", notes: str = ""):
    """Met à jour une entrée existante et rafraîchit updated_at."""
    # TODO: UPDATE passwords SET service=?, username=?, password=?,
    #       url=?, notes=?, updated_at=datetime('now','localtime')
    #       WHERE id=?

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE passwords SET service=?, username=?, password=?, url=?, notes=?, updated_at=datetime('now','localtime') WHERE id=?", (service, username, password, url, notes, pid))
    conn.commit()
    conn.close()


def delete_password(pid: int):
    """Supprime une entrée par son id."""
    # TODO: DELETE FROM passwords WHERE id = ?

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM passwords WHERE id = ?", (pid,))
    conn.commit()
    conn.close()
