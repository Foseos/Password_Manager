"""
views/main_view.py  —  View : Fenêtre principale (CustomTkinter)
"""
import customtkinter as ctk
from tkinter import messagebox
import time

class MainView:
    def __init__(self, root: ctk.CTk, on_search, on_add, on_edit, on_delete, on_copy_password, on_copy_username):
        self._root             = root
        self._on_search        = on_search
        self._on_add           = on_add
        self._on_edit          = on_edit
        self._on_delete        = on_delete
        self._on_copy_password = on_copy_password
        self._on_copy_username = on_copy_username

        root.title("Mon Coffre-fort")
        root.geometry("1000x700")
        root.minsize(800, 500)
        self._center(1000, 700)
        
        self._build()

    def _center(self, w: int, h: int):
        self._root.update_idletasks()
        x = (self._root.winfo_screenwidth()  - w) // 2
        y = (self._root.winfo_screenheight() - h) // 2
        self._root.geometry(f"{w}x{h}+{x}+{y}")

    def _build(self):
        # ─ Main Container
        self.container = ctk.CTkFrame(self._root, fg_color="transparent")
        self.container.pack(fill="both", expand=True)

        # ─ Top Bar
        self.top_bar = ctk.CTkFrame(self.container, height=80, corner_radius=0, fg_color="#1a1a1a")
        self.top_bar.pack(fill="x")
        self.top_bar.pack_propagate(False)

        # Title / Logo
        title_frame = ctk.CTkFrame(self.top_bar, fg_color="transparent")
        title_frame.pack(side="left", padx=30, fill="y", pady=20)
        ctk.CTkLabel(title_frame, text="🔐", font=("Segoe UI", 28)).pack(side="left", padx=(0, 10))
        ctk.CTkLabel(title_frame, text="Mon Coffre", font=("Segoe UI", 24, "bold")).pack(side="left")

        # Search Bar
        search_frame = ctk.CTkFrame(self.top_bar, fg_color="transparent")
        search_frame.pack(side="left", expand=True, fill="y", pady=22)
        
        self._search_var = ctk.StringVar()
        self._search_var.trace_add("write", lambda *_: self._on_search(self._search_var.get().strip()))
        
        search_entry = ctk.CTkEntry(
            search_frame, textvariable=self._search_var, 
            placeholder_text="🔍 Rechercher un compte...", font=("Segoe UI", 14),
            width=350, height=40, corner_radius=20, border_width=1
        )
        search_entry.pack(side="left")

        # Add Button
        add_btn = ctk.CTkButton(
            self.top_bar, text="➕ Nouveau", font=("Segoe UI", 14, "bold"),
            command=self._on_add, height=40, width=120, corner_radius=20,
            fg_color="#10a37f", hover_color="#0b8c6c"
        )
        add_btn.pack(side="right", padx=30, pady=20)

        # ─ Content Area (List of passwords)
        self.content_area = ctk.CTkFrame(self.container, fg_color="transparent")
        self.content_area.pack(fill="both", expand=True, padx=30, pady=20)

        # Header definitions
        headers_frame = ctk.CTkFrame(self.content_area, height=40, fg_color="transparent")
        headers_frame.pack(fill="x", pady=(0, 10), padx=10)
        
        ctk.CTkLabel(headers_frame, text="Service", font=("Segoe UI", 13, "bold"), text_color="gray", width=250, anchor="w").pack(side="left")
        ctk.CTkLabel(headers_frame, text="Identifiant", font=("Segoe UI", 13, "bold"), text_color="gray", width=250, anchor="w").pack(side="left")
        ctk.CTkLabel(headers_frame, text="Dernière modif.", font=("Segoe UI", 13, "bold"), text_color="gray", width=150, anchor="w").pack(side="left")
        ctk.CTkLabel(headers_frame, text="Actions", font=("Segoe UI", 13, "bold"), text_color="gray", anchor="e").pack(side="right", padx=20, expand=True)

        # Scrollable List
        self.list_frame = ctk.CTkScrollableFrame(self.content_area, fg_color="transparent")
        self.list_frame.pack(fill="both", expand=True)

        # Status Bar
        self.status_bar = ctk.CTkFrame(self.container, height=30, corner_radius=0, fg_color="#1a1a1a")
        self.status_bar.pack(fill="x", side="bottom")
        self.status_bar.pack_propagate(False)
        self._status_lbl = ctk.CTkLabel(self.status_bar, text="Prêt", font=("Segoe UI", 12), text_color="gray")
        self._status_lbl.pack(side="left", padx=20, pady=5)
        
    def load_rows(self, rows: list):
        """Reconstruit la liste des mots de passe."""
        # Vider la liste actuelle
        for widget in self.list_frame.winfo_children():
            widget.destroy()

        if not rows:
            ctk.CTkLabel(self.list_frame, text="Aucun compte trouvé.", font=("Segoe UI", 16), text_color="gray").pack(pady=40)
            self.set_status("0 compte")
            return

        for r in rows:
            self._create_row(r)
            
        self.set_status(f"{len(rows)} compte(s)")

    def _create_row(self, r):
        pid = r["id"]
        
        # Row Container
        row = ctk.CTkFrame(self.list_frame, height=60, fg_color=("#e0e0e0", "#2b2b2b"), corner_radius=10)
        row.pack(fill="x", pady=4, padx=5)
        row.pack_propagate(False)

        # Service
        svc_frame = ctk.CTkFrame(row, fg_color="transparent", width=250)
        svc_frame.pack(side="left", fill="y", padx=10)
        svc_frame.pack_propagate(False)
        ctk.CTkLabel(svc_frame, text=r["service"], font=("Segoe UI", 16, "bold"), anchor="w").pack(side="left", fill="x", expand=True)

        # Username
        usr_frame = ctk.CTkFrame(row, fg_color="transparent", width=250)
        usr_frame.pack(side="left", fill="y", padx=10)
        usr_frame.pack_propagate(False)
        ctk.CTkLabel(usr_frame, text=r["username"], font=("Segoe UI", 14), text_color="gray", anchor="w").pack(side="left", fill="x", expand=True)

        # Info additionnelle (Date)
        date_frame = ctk.CTkFrame(row, fg_color="transparent", width=150)
        date_frame.pack(side="left", fill="y", padx=10)
        date_frame.pack_propagate(False)
        date_str = r["updated_at"].split(" ")[0] if r["updated_at"] else ""
        ctk.CTkLabel(date_frame, text=date_str, font=("Segoe UI", 12), text_color="gray", anchor="w").pack(side="left", fill="x", expand=True)

        # Actions
        actions_frame = ctk.CTkFrame(row, fg_color="transparent")
        actions_frame.pack(side="right", fill="y", padx=10)
        
        btn_copy_pwd = ctk.CTkButton(actions_frame, text="📋 Mdp", width=60, height=30, fg_color="#2b5c8f", hover_color="#1a3d63", command=lambda: self._on_copy_password(pid))
        btn_copy_pwd.pack(side="left", padx=4, pady=15)
        
        btn_copy_usr = ctk.CTkButton(actions_frame, text="👤 Login", width=60, height=30, fg_color="#444444", hover_color="#333333", command=lambda: self._on_copy_username(pid))
        btn_copy_usr.pack(side="left", padx=4, pady=15)
        
        btn_edit = ctk.CTkButton(actions_frame, text="✏️", width=30, height=30, fg_color="transparent", hover_color="#444444", border_width=1, command=lambda: self._on_edit(pid))
        btn_edit.pack(side="left", padx=4, pady=15)
        
        btn_delete = ctk.CTkButton(actions_frame, text="🗑", width=30, height=30, fg_color="transparent", hover_color="#e74c3c", border_width=1, text_color="#e74c3c", command=lambda: self._on_delete(pid))
        btn_delete.pack(side="left", padx=4, pady=15)

    def set_status(self, message: str, color: str = "#10a37f"):
        self._status_lbl.configure(text=message, text_color=color)
        self._root.after(4000, lambda: self._status_lbl.configure(text="Prêt", text_color="gray"))

    def show_info(self, message: str):
        messagebox.showinfo("Info", message, parent=self._root)

    def show_error(self, message: str):
        messagebox.showerror("Erreur", message, parent=self._root)

    def confirm_delete(self, service: str) -> bool:
        return messagebox.askyesno("Confirmation", f"Supprimer le compte « {service} » ?", parent=self._root)
