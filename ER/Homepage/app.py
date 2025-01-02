import customtkinter as ctk
from login import Login
from area_paziente import AreaPaziente
from area_gestore import AreaGestore

class App:
    def __init__(self, root):
        ctk.set_appearance_mode("dark")  # Tema chiaro o scuro: "dark" o "light"
        ctk.set_default_color_theme("dark-blue")  # Tema colore principale: "dark-blue"
        
        self.root = root
        self.root.title("Sito Ospedaliero")
        self.root.geometry("900x700")
        self.languages = {
            "Italiano": {
                "title": "Benvenuto nel nostro Sistema Ospedaliero",
                "privacy_button": "Informativa sulla Privacy",
                "terms_button": "Termini e Condizioni",
                "login_button": "Login / Registrati",
                "copyright": "© 2024 LifePulse. Tutti i diritti riservati.",
            }
        }
        self.current_language = "Italiano"
        self.home_page()

    def home_page(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        # Navbar in alto
        self.navbar_frame = ctk.CTkFrame(self.root, height=60, corner_radius=0)
        self.navbar_frame.pack(fill="x")

        logo_label = ctk.CTkLabel(self.navbar_frame, text="LifePulse", font=("Arial", 22, "bold"))
        logo_label.pack(side="left", padx=20)

        login_button = ctk.CTkButton(self.navbar_frame, text=self.languages[self.current_language]["login_button"], command=self.open_login)
        login_button.pack(side="right", padx=10)

        # Sezione Introduzione
        intro_label = ctk.CTkLabel(self.root, text=self.languages[self.current_language]["title"], font=("Arial", 22, "bold"))
        intro_label.pack(pady=20)

        # Footer con informazioni
        footer_frame = ctk.CTkFrame(self.root, height=120, corner_radius=0)
        footer_frame.pack(side="bottom", fill="x", pady=20)

        privacy_button = ctk.CTkButton(footer_frame, text=self.languages[self.current_language]["privacy_button"], command=self.show_privacy)
        privacy_button.pack(side="left", padx=20)

        terms_button = ctk.CTkButton(footer_frame, text=self.languages[self.current_language]["terms_button"], command=self.show_terms)
        terms_button.pack(side="left", padx=20)

        copyright_label = ctk.CTkLabel(footer_frame, text=self.languages[self.current_language]["copyright"], font=("Arial", 10))
        copyright_label.pack(side="bottom", pady=10)

    def open_login(self):
        login_window = ctk.CTkToplevel(self.root)
        login = Login(login_window, self)

    def open_area_paziente(self, username, data_nascita):
        area_paziente_window = ctk.CTkToplevel(self.root)
        area_paziente = AreaPaziente(area_paziente_window, username, data_nascita)
        self.root.withdraw()

    def open_area_gestore(self, username):
        area_gestore_window = ctk.CTkToplevel(self.root)
        area_gestore = AreaGestore(area_gestore_window, username)

    def show_privacy(self):
        privacy_window = ctk.CTkToplevel(self.root)
        privacy_window.title(self.languages[self.current_language]["privacy_button"])
        privacy_window.geometry("600x400")

        privacy_title = ctk.CTkLabel(privacy_window, text=self.languages[self.current_language]["privacy_button"], font=("Arial", 18, "bold"))
        privacy_title.pack(pady=20)

        privacy_text = ctk.CTkLabel(privacy_window, text="La tua privacy è importante per noi. Leggi le nostre politiche qui...", font=("Arial", 14))
        privacy_text.pack(pady=20)

    def show_terms(self):
        terms_window = ctk.CTkToplevel(self.root)
        terms_window.title(self.languages[self.current_language]["terms_button"])
        terms_window.geometry("600x400")

        terms_title = ctk.CTkLabel(terms_window, text=self.languages[self.current_language]["terms_button"], font=("Arial", 18, "bold"))
        terms_title.pack(pady=20)

        terms_text = ctk.CTkLabel(terms_window, text="Leggi i nostri termini e condizioni per l'uso del sito...", font=("Arial", 14))
        terms_text.pack(pady=20)

if __name__ == "__main__":
    root = ctk.CTk()
    app = App(root)
    root.mainloop()
