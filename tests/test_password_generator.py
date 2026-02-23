"""
tests/test_password_generator.py
"""
import pytest
from models.password_generator import generate_password, password_strength

def test_generate_password_length():
    pwd = generate_password(length=20)
    assert len(pwd) == 20

def test_generate_password_requirements():
    pwd = generate_password(
        length=16,
        use_uppercase=True,
        use_digits=True,
        use_symbols=True
    )
    # Vérifie qu'il y a au moins un des caractères demandés
    has_upper = any(c.isupper() for c in pwd)
    has_digit = any(c.isdigit() for c in pwd)
    has_symbol = any(not c.isalnum() for c in pwd)
    
    assert has_upper, "Le mot de passe devrait contenir une majuscule"
    assert has_digit, "Le mot de passe devrait contenir un chiffre"
    assert has_symbol, "Le mot de passe devrait contenir un symbole"

def test_password_strength():
    # Faible (trop court)
    label, color = password_strength("short")
    assert label == "Faible"
    
    # Moyen (juste long mais pas complexe)
    label, color = password_strength("longpasswordwithoutnumbers3")
    assert label == "Moyen"
    
    # Fort (longueur + maj + chiffre + symbole)
    label, color = password_strength("Tr3sF0rt!Passw0rd")
    assert label == "Fort"
