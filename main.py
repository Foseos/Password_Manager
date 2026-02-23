"""
main.py — Point d'entrée de l'application (MVC)
"""

import customtkinter as ctk

from models import database as db
from controllers.auth_controller import AuthController
from controllers.password_controller import PasswordController
from views.login_view import LoginView
from views.main_view import MainView
from views.password_dialog_view import PasswordDialogView
from models.password_generator import password_strength

# Configuration globale CustomTkinter (Thème sombre + accent vert type Dashlane)
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")


def main():
    # 1. Initialiser la BDD (crée les tables si première exécution)
    db.init_db()

    # 2. Fenêtre racine (cachée jusqu'à la connexion)
    root = ctk.CTk()
    root.withdraw()

    auth_ctrl = AuthController()

    # ── Callback déclenché quand l'utilisateur valide la LoginView ────────────
    def on_login_submit(password: str, confirm: str):
        if auth_ctrl.master_exists():
            success, error, fernet = auth_ctrl.login(password)
        else:
            success, error, fernet = auth_ctrl.create_master(password, confirm)

        if not success:
            login_view.show_error(error)
            return

        # 3. Connexion réussie → fermer la LoginView et ouvrir la MainView
        login_view.close()
        root.deiconify()
        _start_main(fernet)

    # 4. Afficher la LoginView
    login_view = LoginView(root, not auth_ctrl.master_exists(), on_login_submit)

    # ── Construction de la MainView après authentification ────────────────────
    def _start_main(fernet):
        pwd_ctrl = PasswordController(fernet)
        main_view = None  # Correction pour éviter l'erreur Free Variable

        def refresh(query: str = ""):
            rows = pwd_ctrl.search(query) if query else pwd_ctrl.get_all()
            main_view.load_rows(rows)

        def on_add():
            def save(svc, user, plain_pwd, url, notes):
                pwd_ctrl.add(svc, user, plain_pwd, url, notes)
                refresh(main_view._search_var.get().strip())
                main_view.set_status("✅ Ajouté avec succès")

            PasswordDialogView(
                root, record=None,
                on_save=save,
                on_generate=lambda: pwd_ctrl.generate(),
                on_strength=password_strength,
            )

        def on_edit(pid: int):
            record_row = pwd_ctrl.get_by_id(pid)
            ok, plaintext = pwd_ctrl.decrypt_password(record_row["password"])
            record = dict(record_row)
            record["plaintext"] = plaintext if ok else ""

            def save(svc, user, plain_pwd, url, notes):
                pwd_ctrl.update(pid, svc, user, plain_pwd, url, notes)
                refresh(main_view._search_var.get().strip())
                main_view.set_status("✅ Modifié avec succès", "#3498db")

            PasswordDialogView(
                root, record=record,
                on_save=save,
                on_generate=lambda: pwd_ctrl.generate(),
                on_strength=password_strength,
            )

        def on_delete(pid: int):
            record = pwd_ctrl.get_by_id(pid)
            if main_view.confirm_delete(record["service"]):
                pwd_ctrl.delete(pid)
                refresh(main_view._search_var.get().strip())
                main_view.set_status("🗑 Supprimé", "#e74c3c")

        def on_copy_password(pid: int):
            import pyperclip
            record = pwd_ctrl.get_by_id(pid)
            ok, plaintext = pwd_ctrl.decrypt_password(record["password"])
            if ok:
                pyperclip.copy(plaintext)
                main_view.set_status("📋 Mot de passe copié !")
            else:
                main_view.show_error("Impossible de déchiffrer ce mot de passe.")

        def on_copy_username(pid: int):
            import pyperclip
            record = pwd_ctrl.get_by_id(pid)
            pyperclip.copy(record["username"])
            main_view.set_status("👤 Identifiant copié !")

        main_view = MainView(
            root,
            on_search=refresh,
            on_add=on_add,
            on_edit=on_edit,
            on_delete=on_delete,
            on_copy_password=on_copy_password,
            on_copy_username=on_copy_username,
        )
        refresh()

    root.mainloop()


if __name__ == "__main__":
    main()
