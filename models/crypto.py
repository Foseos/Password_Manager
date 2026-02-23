"""
models/crypto.py

RÔLE (Model) : Tout ce qui concerne le chiffrement des données.
Aucune dépendance vers les autres couches (ni views, ni controllers).

BIBLIOTHÈQUE : cryptography
    pip install cryptography

────────────────────────────────────────────────────────────────
ÉTAPE 1 — Générer un sel aléatoire
────────────────────────────────────────────────────────────────
Un "sel" est une suite d'octets aléatoires qu'on mélange avec
le mot de passe pour que deux mots de passe identiques donnent
des clés différentes.

    import os
    sel = os.urandom(32)   # 32 octets = 256 bits

────────────────────────────────────────────────────────────────
ÉTAPE 2 — Dériver une clé depuis le mot de passe maître (PBKDF2)
────────────────────────────────────────────────────────────────
PBKDF2 = Password-Based Key Derivation Function 2.
On applique SHA-256 des milliers de fois pour rendre le brute-force
très coûteux.

    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.backends import default_backend
    import base64

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,           # taille de la clé en octets
        salt=sel,
        iterations=480_000,  # nb d'itérations (OWASP recommande ≥ 210 000)
        backend=default_backend(),
    )
    cle = base64.urlsafe_b64encode(kdf.derive(password.encode()))

────────────────────────────────────────────────────────────────
ÉTAPE 3 — Créer une instance Fernet avec cette clé
────────────────────────────────────────────────────────────────
Fernet garantit un chiffrement AES-128-CBC + HMAC-SHA256.

    from cryptography.fernet import Fernet
    f = Fernet(cle)

────────────────────────────────────────────────────────────────
ÉTAPE 4 — Chiffrer / Déchiffrer
────────────────────────────────────────────────────────────────
    token = f.encrypt(b"mon secret")   # retourne bytes
    clair = f.decrypt(token)           # retourne bytes → .decode() pour str

────────────────────────────────────────────────────────────────
À TOI DE JOUER — Implémente les fonctions ci-dessous
────────────────────────────────────────────────────────────────
"""

import os
import base64
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet


def generate_salt() -> bytes:
    """Génère et retourne un sel aléatoire de 32 octets."""
    # TODO: utilise os.urandom(32)
    return os.urandom(32)


def derive_key(password: str, salt: bytes) -> bytes:
    """
    Dérive une clé Fernet (base64) à partir du mot de passe et du sel.
    Retourne la clé encodée en base64 (bytes).
    """
    # TODO: crée un PBKDF2HMAC avec SHA256, length=32, 480_000 itérations
    # TODO: retourne base64.urlsafe_b64encode(kdf.derive(password.encode()))
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480_000,
        backend=default_backend(),
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))


def get_fernet(password: str, salt: bytes) -> Fernet:
    """Retourne une instance Fernet prête à l'emploi."""
    # TODO: appelle derive_key puis Fernet(cle)
    key = derive_key(password, salt)
    return Fernet(key)


def encrypt(plaintext: str, fernet: Fernet) -> str:
    """Chiffre une chaîne et retourne le token sous forme de str."""
    # TODO: fernet.encrypt(plaintext.encode()).decode()
    return fernet.encrypt(plaintext.encode()).decode()


def decrypt(token: str, fernet: Fernet) -> str:
    """Déchiffre un token str et retourne la chaîne originale."""
    # TODO: fernet.decrypt(token.encode()).decode()
    return fernet.decrypt(token.encode()).decode()
