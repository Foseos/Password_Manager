"""
controllers/auth_controller.py

RÔLE (Controller) : Orchestrer l'authentification entre la View et les Models.
Il reçoit les actions de la LoginView, appelle les Models, et communique
le résultat à la View.

════════════════════════════════════════════════════════════════
PATTERN UTILISÉ : le Controller reçoit les données brutes de la View,
                  appelle les fonctions du Model, et retourne le résultat.
════════════════════════════════════════════════════════════════

IMPORTS NÉCESSAIRES :
    from models import database as db
    from models import crypto
    from cryptography.fernet import Fernet

════════════════════════════════════════════════════════════════
À TOI DE JOUER — Crée la classe AuthController ci-dessous
════════════════════════════════════════════════════════════════

La classe doit exposer ces méthodes publiques :

┌─────────────────────────────────────────────────────────────┐
│ master_exists() -> bool                                      │
│   → Délègue simplement à db.master_exists()                  │
├─────────────────────────────────────────────────────────────┤
│ create_master(password: str, confirm: str)                   │
│     -> tuple[bool, str, Fernet | None]                       │
│   → Valide que password == confirm et len >= 6               │
│   → Si ok : génère un sel (crypto.generate_salt()),          │
│             sauvegarde (db.save_master()),                   │
│             retourne (True, "", fernet)                      │
│   → Si erreur : retourne (False, "message d'erreur", None)  │
├─────────────────────────────────────────────────────────────┤
│ login(password: str)                                         │
│     -> tuple[bool, str, Fernet | None]                       │
│   → Appelle db.verify_master(password)                       │
│   → Si valide : construit le Fernet, retourne (True,"",f)   │
│   → Si invalide : retourne (False, "Mot de passe incorrect") │
└─────────────────────────────────────────────────────────────┘

Hints :
- La Fernet key dépend du mot de passe ET du sel → crypto.get_fernet(pwd, salt)
- Le Controller ne fait JAMAIS d'affichage (pas de print, pas de messagebox)
- Il retourne des données, c'est la View qui affiche

"""

from models import database as db
from models import crypto
from cryptography.fernet import Fernet


class AuthController:

    def master_exists(self) -> bool:
        # TODO
        return db.master_exists()

    def create_master(self, password: str, confirm: str) -> tuple[bool, str, Fernet | None]:
        # TODO
        if password != confirm:
            return False, "Les mots de passe ne correspondent pas", None
        if len(password) < 6:
            return False, "Le mot de passe doit contenir au moins 6 caractères", None
        salt = crypto.generate_salt()
        db.save_master(password, salt)
        fernet = crypto.get_fernet(password, salt)
        return True, "", fernet

    def login(self, password: str) -> tuple[bool, str, Fernet | None]:
        is_valid, salt = db.verify_master(password)
        if not is_valid:
            return False, "Mot de passe incorrect", None
        fernet = crypto.get_fernet(password, salt)
        return True, "", fernet
