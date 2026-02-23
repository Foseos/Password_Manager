"""
views/password_dialog_view.py  —  View : Dialogue Ajouter / Modifier (CustomTkinter)
"""
import customtkinter as ctk
from tkinter import messagebox

class PasswordDialogView(ctk.CTkToplevel):
    def __init__(self, master, record: dict | None, on_save, on_generate, on_strength):
        super().__init__(master)
        self._record      = record
        self._on_save     = on_save
        self._on_generate = on_generate
        self._on_strength = on_strength

        self.title("Modifier" if record else "Ajouter un compte")
        self.resizable(False, False)
        
        # Rend la fenêtre modale
        self.transient(master)
        self.grab_set()
        self._center(450, 600)
        self._build()
        
        if record:
            self._prefill(record)

    def _center(self, w: int, h: int):
        self.update_idletasks()
        x = (self.winfo_screenwidth()  - w) // 2
        y = (self.winfo_screenheight() - h) // 2
        self.geometry(f"{w}x{h}+{x}+{y}")

    def _build(self):
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True, padx=30, pady=25)

        title_text = "✏️ Modifier le compte" if self._record else "➕ Nouveau compte"
        ctk.CTkLabel(self.main_frame, text=title_text, font=("Segoe UI", 22, "bold")).pack(pady=(0, 20), anchor="w")

        # Champs texte
        self._svc_var  = self._add_field("Service / Application *", "ex: GitHub, Google...")
        self._user_var = self._add_field("Nom d'utilisateur / Email *", "ex: user@example.com")
        self._url_var  = self._add_field("URL (optionnel)", "ex: https://github.com")

        # Mot de passe + boutons
        ctk.CTkLabel(self.main_frame, text="Mot de passe *", font=("Segoe UI", 12, "bold"), text_color="gray").pack(anchor="w", pady=(10, 2))
        pwd_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        pwd_frame.pack(fill="x", pady=(0, 2))

        self._pwd_var = ctk.StringVar()
        self._pwd_var.trace_add("write", self._update_strength)
        self._show_var = ctk.BooleanVar(value=False)

        self._pwd_entry = ctk.CTkEntry(
            pwd_frame, textvariable=self._pwd_var, show="•",
            font=("Consolas", 14), height=35, placeholder_text="Votre mot de passe secret"
        )
        self._pwd_entry.pack(side="left", fill="x", expand=True)

        self.toggle_btn = ctk.CTkButton(
            pwd_frame, width=40, text="👁", font=("Segoe UI", 16),
            command=self._toggle_show, height=35, fg_color="#333333", hover_color="#555555"
        )
        self.toggle_btn.pack(side="left", padx=(5, 0))

        self.gen_btn = ctk.CTkButton(
            pwd_frame, width=80, text="⚙ Générer", font=("Segoe UI", 12, "bold"),
            command=self._generate, height=35, fg_color="#2b5c8f", hover_color="#1a3d63"
        )
        self.gen_btn.pack(side="left", padx=(5, 0))

        # Jauge de force
        self._strength_lbl = ctk.CTkLabel(self.main_frame, text="", font=("Segoe UI", 11, "bold"))
        self._strength_lbl.pack(anchor="w", pady=(0, 10))

        # Notes
        ctk.CTkLabel(self.main_frame, text="Notes (optionnel)", font=("Segoe UI", 12, "bold"), text_color="gray").pack(anchor="w")
        self._notes = ctk.CTkTextbox(self.main_frame, height=80, font=("Segoe UI", 13), corner_radius=8)
        self._notes.pack(fill="x", pady=(2, 20))

        # Bouton Enregistrer
        self.save_btn = ctk.CTkButton(
            self.main_frame, text="Enregistrer", font=("Segoe UI", 14, "bold"),
            height=45, fg_color="#10a37f", hover_color="#0b8c6c",
            command=self._submit
        )
        self.save_btn.pack(fill="x")

    def _add_field(self, label: str, placeholder: str) -> ctk.StringVar:
        ctk.CTkLabel(self.main_frame, text=label, font=("Segoe UI", 12, "bold"), text_color="gray").pack(anchor="w", pady=(5, 2))
        var = ctk.StringVar()
        entry = ctk.CTkEntry(self.main_frame, textvariable=var, font=("Segoe UI", 14), height=35, placeholder_text=placeholder)
        entry.pack(fill="x", pady=(0, 5))
        return var

    def _prefill(self, record: dict):
        self._svc_var.set(record.get("service", ""))
        self._user_var.set(record.get("username", ""))
        self._url_var.set(record.get("url", "") or "")
        self._pwd_var.set(record.get("plaintext", ""))
        notes = record.get("notes", "") or ""
        if notes:
            self._notes.insert("0.0", notes)

    def _toggle_show(self):
        self._show_var.set(not self._show_var.get())
        self._pwd_entry.configure(show="" if self._show_var.get() else "•")

    def _generate(self):
        pwd = self._on_generate()
        self._pwd_var.set(pwd)
        self._show_var.set(True)
        self._pwd_entry.configure(show="")

    def _update_strength(self, *_):
        pwd = self._pwd_var.get()
        if pwd:
            label, color = self._on_strength(pwd)
            self._strength_lbl.configure(text=f"Force : {label}", text_color=color)
        else:
            self._strength_lbl.configure(text="")

    def _submit(self):
        svc   = self._svc_var.get().strip()
        user  = self._user_var.get().strip()
        pwd   = self._pwd_var.get()
        url   = self._url_var.get().strip()
        notes = self._notes.get("0.0", "end").strip()

        if not svc or not user or not pwd:
            messagebox.showerror("Erreur", "Les champs marqués * sont obligatoires.", parent=self)
            return

        self._on_save(svc, user, pwd, url, notes)
        self.destroy()

    def show_error(self, message: str):
        messagebox.showerror("Erreur", message, parent=self)
