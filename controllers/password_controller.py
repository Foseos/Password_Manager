"""
controllers/password_controller.py

RÔLE (Controller) : Orchestrer toutes les opérations sur les mots de passe.
Il fait le lien entre la MainView / PasswordDialogView et les Models (database, crypto).

════════════════════════════════════════════════════════════════
IMPORTANT : Le controller reçoit le Fernet au constructeur.
Le Fernet est créé une seule fois à la connexion (dans AuthController)
et passé aux autres controllers pour chiffrer/déchiffrer.
════════════════════════════════════════════════════════════════

IMPORTS NÉCESSAIRES :
    from models import database as db
    from models import crypto
    from models.password_generator import generate_password
    from cryptography.fernet import Fernet, InvalidToken

════════════════════════════════════════════════════════════════
À TOI DE JOUER — Crée la classe PasswordController ci-dessous
════════════════════════════════════════════════════════════════

__init__(self, fernet: Fernet)
    → Stocke le fernet dans self._fernet

┌──────────────────────────────────────────────────────────────┐
│ get_all() -> list                                             │
│   → Retourne db.get_all_passwords()                          │
├──────────────────────────────────────────────────────────────┤
│ search(query: str) -> list                                    │
│   → Si query vide → get_all(), sinon db.search_passwords(q)  │
├──────────────────────────────────────────────────────────────┤
│ add(service, username, plaintext_pwd, url, notes)            │
│     -> int  (l'id de la nouvelle entrée)                     │
│   → Chiffre plaintext_pwd avec crypto.encrypt()              │
│   → Appelle db.add_password() et retourne l'id               │
├──────────────────────────────────────────────────────────────┤
│ update(pid, service, username, plaintext_pwd, url, notes)    │
│   → Chiffre le nouveau mot de passe                          │
│   → Appelle db.update_password()                             │
├──────────────────────────────────────────────────────────────┤
│ delete(pid: int)                                             │
│   → Appelle db.delete_password(pid)                          │
├──────────────────────────────────────────────────────────────┤
│ get_by_id(pid: int)                                          │
│   → Retourne db.get_password_by_id(pid)                      │
├──────────────────────────────────────────────────────────────┤
│ decrypt_password(encrypted: str) -> tuple[bool, str]         │
│   → Essaie crypto.decrypt(encrypted, self._fernet)           │
│   → Retourne (True, plaintext) si ok                         │
│   → Retourne (False, "") si InvalidToken                     │
│     (le mot de passe maître ne correspond pas aux données)   │
├──────────────────────────────────────────────────────────────┤
│ generate(length=16, uppercase=True,                          │
│          digits=True, symbols=True) -> str                   │
│   → Délègue à generate_password(...)                         │
└──────────────────────────────────────────────────────────────┘

Hints :
- Ne jamais stocker un mot de passe EN CLAIR en base
- InvalidToken est levé si le Fernet ne correspond pas → attrape-le avec try/except
- Le controller ne fait jamais d'affichage

"""

from models import database as db
from models import crypto
from models.password_generator import generate_password
from cryptography.fernet import Fernet, InvalidToken


class PasswordController:

    def __init__(self, fernet: Fernet):
        # TODO: stocke fernet dans self._fernet
        self._fernet = fernet

    def get_all(self) -> list:
        # TODO
        return db.get_all_passwords()

    def search(self, query: str) -> list:
        # TODO
        return db.search_passwords(query)

    def add(self, service: str, username: str, plaintext_pwd: str,
            url: str = "", notes: str = "") -> int:
        # TODO: chiffre puis stocke
        encrypted_pwd = crypto.encrypt(plaintext_pwd, self._fernet)
        return db.add_password(service, username, encrypted_pwd, url, notes)

    def update(self, pid: int, service: str, username: str,
               plaintext_pwd: str, url: str = "", notes: str = ""):
        # TODO: chiffre puis met à jour
        encrypted_pwd = crypto.encrypt(plaintext_pwd, self._fernet)
        db.update_password(pid, service, username, encrypted_pwd, url, notes)

    def delete(self, pid: int):
        # TODO
        db.delete_password(pid)

    def get_by_id(self, pid: int):
        # TODO
        return db.get_password_by_id(pid)

    def decrypt_password(self, encrypted: str) -> tuple[bool, str]:
        # TODO: try/except InvalidToken
        try:
            return True, crypto.decrypt(encrypted, self._fernet)
        except InvalidToken:
            return False, ""

    def generate(self, length: int = 16, uppercase: bool = True,
                 digits: bool = True, symbols: bool = True) -> str:
        # TODO: délègue à generate_password(...)
        return generate_password(length, uppercase, digits, symbols)
