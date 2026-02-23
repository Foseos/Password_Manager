"""
models/password_generator.py

RÔLE (Model) : Génération de mots de passe sécurisés et évaluation de leur force.
Aucune dépendance externe — uniquement la bibliothèque standard Python.

════════════════════════════════════════════════════════════════
CONCEPTS À CONNAÎTRE
════════════════════════════════════════════════════════════════

1. POURQUOI "secrets" et pas "random" ?
   - random est PRÉVISIBLE (seed basé sur le temps).
   - secrets utilise l'entropie du système d'exploitation → cryptographiquement sûr.

   import secrets
   import string

   alphabet = string.ascii_letters + string.digits + "!@#$%"
   mdp = "".join(secrets.choice(alphabet) for _ in range(16))

2. GARANTIR AU MOINS 1 DE CHAQUE TYPE
   Pour éviter qu'un mot de passe généré ne contienne aucun chiffre
   par malchance, force au moins un caractère de chaque catégorie :

   obligatoires = [
       secrets.choice(string.ascii_lowercase),
       secrets.choice(string.ascii_uppercase),
       secrets.choice(string.digits),
   ]
   reste = [secrets.choice(alphabet) for _ in range(length - len(obligatoires))]
   # Mélange pour ne pas toujours avoir les obligatoires au début
   secrets.SystemRandom().shuffle(obligatoires + reste)

3. ÉVALUATION DE LA FORCE
   Attribue des points selon des critères (longueur, types de caractères) :
   - ≥ 8 caractères   → +1 point
   - ≥ 12 caractères  → +1 point
   - Contient majuscule → +1 point
   - Contient chiffre   → +1 point
   - Contient symbole   → +1 point
   Total ≤ 2 → "Faible" | ≤ 4 → "Moyen" | > 4 → "Fort"

════════════════════════════════════════════════════════════════
À TOI DE JOUER — Implémente les fonctions ci-dessous
════════════════════════════════════════════════════════════════
"""

import secrets
import string


def generate_password(
    length: int = 16,
    use_uppercase: bool = True,
    use_digits: bool = True,
    use_symbols: bool = True,
) -> str:
    """
    Génère un mot de passe cryptographiquement sûr.

    Args:
        length:        Longueur souhaitée (minimum 8).
        use_uppercase: Inclure des majuscules (A-Z).
        use_digits:    Inclure des chiffres (0-9).
        use_symbols:   Inclure des caractères spéciaux.

    Returns:
        Le mot de passe généré sous forme de str.

    Hints:
        - Commence par length = max(8, length)
        - Construis l'alphabet en partant de string.ascii_lowercase
        - Ajoute chaque catégorie activée à l'alphabet ET aux obligatoires
        - Complète jusqu'à `length` caractères avec secrets.choice(alphabet)
        - Mélange le tout avec secrets.SystemRandom().shuffle(...)
        - Retourne "".join(liste)
    """
    length = max(8, length)
    
    # 1. Construit l'alphabet
    alphabet = string.ascii_lowercase

    obligatoires = [secrets.choice(string.ascii_lowercase)]  # ← toujours au moins 1 minuscule
    if use_uppercase:
        alphabet += string.ascii_uppercase
        obligatoires.append(secrets.choice(string.ascii_uppercase))  # ← 1 maj garantie
    if use_digits:
        alphabet += string.digits
        obligatoires.append(secrets.choice(string.digits))           # ← 1 chiffre garanti
    if use_symbols:
        symbols = "!@#$%^&*()-_=+[]{}|;:,.<>?"
        alphabet += symbols
        obligatoires.append(secrets.choice(symbols))                 # ← 1 symbole garanti

    # 2. Complète jusqu'à `length`
    reste = [secrets.choice(alphabet) for _ in range(length - len(obligatoires))]
    
    # 3. Mélange
    tout = obligatoires + reste
    secrets.SystemRandom().shuffle(tout)
    
    return "".join(tout)


def password_strength(password: str) -> tuple[str, str]:
    """
    Évalue la force d'un mot de passe.

    Returns:
        Un tuple (niveau: str, couleur_hex: str)
        Exemples : ("Faible", "#e74c3c") | ("Moyen", "#f39c12") | ("Fort", "#2ecc71")

    Hints:
        - Initialise score = 0
        - Vérifie chaque critère avec if/any() et incrémente score
        - any(c.isupper() for c in password) → True si au moins une majuscule
        - any(c in "!@#$%..." for c in password) → True si au moins un symbole
    """
    score = 0

    if len(password) >= 8:
        score += 1
    if len(password) >= 12:
        score += 1
    if any(c.isupper() for c in password):
        score += 1
    if any(c.isdigit() for c in password):
        score += 1
    if any(c in "!@#$%^&*()-_=+[]{}|;:,.<>?" for c in password):
        score += 1

    if score <= 2:
        return "Faible", "#e74c3c"
    elif score <= 4:
        return "Moyen", "#f39c12"
    else:
        return "Fort", "#2ecc71"
