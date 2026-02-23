"""
views/login_view.py  —  View : Fenêtre de connexion / création du mot de passe maître (CustomTkinter)
"""

import customtkinter as ctk
from tkinter import messagebox


class LoginView(ctk.CTkToplevel):
    """
    Fenêtre modale de connexion.
    Utilise CustomTkinter pour un rendu moderne type Dashlane.
    """

    def __init__(self, master: ctk.CTk, is_new: bool, on_submit):
        super().__init__(master)
        self._is_new    = is_new
        self._on_submit = on_submit

        self.title("Authentification")
        self.resizable(False, False)
        
        # Rend la fenêtre modale et s'assure qu'elle est au premier plan
        self.transient(master)
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", master.destroy)
        self._center(400, 420 if is_new else 350)
        
        self._build()

    def _center(self, w: int, h: int):
        self.update_idletasks()
        x = (self.winfo_screenwidth() - w) // 2
        y = (self.winfo_screenheight() - h) // 2
        self.geometry(f"{w}x{h}+{x}+{y}")

    def _build(self):
        # ─ Main Container
        self.main_frame = ctk.CTkFrame(self, corner_radius=15, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True, padx=40, pady=30)

        # ─ Icône / Titre
        icon_label = ctk.CTkLabel(self.main_frame, text="🔐", font=("Segoe UI", 48))
        icon_label.pack(pady=(0, 10))

        title_text = "Bienvenue !" if self._is_new else "Bon retour !"
        subtitle = "Créez votre mot de passe maître" if self._is_new else "Entrez votre mot de passe maître"
        
        ctk.CTkLabel(self.main_frame, text=title_text, font=("Segoe UI", 24, "bold")).pack()
        ctk.CTkLabel(self.main_frame, text=subtitle, font=("Segoe UI", 12), text_color="gray").pack(pady=(0, 20))

        # ─ Champs
        self._pwd_var = ctk.StringVar()
        self.pwd_entry = ctk.CTkEntry(
            self.main_frame, 
            textvariable=self._pwd_var, 
            show="•",
            placeholder_text="Mot de passe maître",
            height=40, 
            corner_radius=8,
            font=("Consolas", 14)
        )
        self.pwd_entry.pack(fill="x", pady=(10, 10))
        self.pwd_entry.focus()

        self._confirm_var = ctk.StringVar()
        if self._is_new:
            self.confirm_entry = ctk.CTkEntry(
                self.main_frame, 
                textvariable=self._confirm_var, 
                show="•",
                placeholder_text="Confirmez le mot de passe",
                height=40, 
                corner_radius=8,
                font=("Consolas", 14)
            )
            self.confirm_entry.pack(fill="x", pady=(0, 20))
        else:
            # Espace supplémentaire pour centrer un peu mieux en mode login
            ctk.CTkFrame(self.main_frame, height=10, fg_color="transparent").pack()

        # ─ Bouton de validation
        btn_text = "Créer mon coffre" if self._is_new else "Déverrouiller"
        self.submit_btn = ctk.CTkButton(
            self.main_frame, 
            text=btn_text, 
            command=self._submit,
            height=45,
            corner_radius=8,
            font=("Segoe UI", 14, "bold"),
            fg_color="#10a37f", hover_color="#0b8c6c"
        )
        self.submit_btn.pack(fill="x", pady=(10, 0))

        self.bind("<Return>", lambda _: self._submit())

    def _submit(self):
        pwd     = self._pwd_var.get().strip()
        confirm = self._confirm_var.get().strip()
        if not pwd:
            self.show_error("Veuillez saisir un mot de passe.")
            return
        self._on_submit(pwd, confirm)

    def show_error(self, message: str):
        messagebox.showerror("Erreur", message, parent=self)

    def show_success(self, message: str):
        messagebox.showinfo("Succès", message, parent=self)

    def close(self):
        self.destroy()
