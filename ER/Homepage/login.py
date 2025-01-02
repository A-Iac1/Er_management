import customtkinter as ctk
from tkinter import messagebox
from user_manager import validate_user, save_user

class Login:
	def __init__(self, root, app):
		ctk.set_appearance_mode("dark")
		ctk.set_default_color_theme("green")

		self.root = root
		self.root.title("Login")
		self.root.geometry("400x400")
		self.app = app

		# Titolo
		self.title = ctk.CTkLabel(self.root, text="Login", font=("Arial", 18))
		self.title.pack(pady=20)

		# Username
		self.username_label = ctk.CTkLabel(self.root, text="Username")
		self.username_label.pack(pady=5)
		self.username_entry = ctk.CTkEntry(self.root, placeholder_text="Inserisci username")
		self.username_entry.pack(pady=5)

		# Password
		self.password_label = ctk.CTkLabel(self.root, text="Password")
		self.password_label.pack(pady=5)
		self.password_entry = ctk.CTkEntry(self.root, placeholder_text="Inserisci password", show="*")
		self.password_entry.pack(pady=5)

		# Pulsante Login
		self.login_button = ctk.CTkButton(self.root, text="Login", command=self.login)
		self.login_button.pack(pady=20)

		# Pulsante Registrazione
		self.register_button = ctk.CTkButton(self.root, text="Registrati", command=self.switch_to_register)
		self.register_button.pack(pady=10)

		# Componenti di registrazione (inizialmente invisibili)
		self.role_label = ctk.CTkLabel(self.root, text="Seleziona il tuo ruolo")
		self.role_combobox = ctk.CTkComboBox(self.root, values=["Paziente", "Gestore"])
		self.role_combobox.set("Paziente")

		self.data_nascita_label = ctk.CTkLabel(self.root, text="Data di nascita (DD/MM/YYYY):")
		self.data_nascita_entry = ctk.CTkEntry(self.root, placeholder_text="Inserisci data di nascita")

	def switch_to_register(self):
		"""Passa alla modalità registrazione."""
		self.root.title("Registrazione")
		self.root.geometry("400x500")
		self.title.configure(text="Registrazione")

		# Aggiungi ruolo sopra al pulsante di registrazione
		self.role_label.pack(pady=5)
		self.role_combobox.pack(pady=5)

		# Aggiungi data di nascita sopra al pulsante di registrazione
		self.data_nascita_label.pack(pady=5)
		self.data_nascita_entry.pack(pady=5)

		# Modifica pulsante per diventare "Registrati"
		self.login_button.configure(text="Registrati", command=self.register)
		self.login_button.pack(side="bottom",pady=20)
		# Nascondi il pulsante di registrazione originale
		self.register_button.pack_forget()

	def login(self):
		"""Gestisce il login."""
		username = self.username_entry.get()
		password = self.password_entry.get()

		role, data_nascita = self.get_role(username, password)
		if role:
			if role == "Paziente":
				self.app.open_area_paziente(username, data_nascita)
			elif role == "Gestore":
				self.app.open_area_gestore(username)
			self.root.destroy()
		else:
			messagebox.showerror("Errore", "Credenziali non valide")

	def register(self):
		"""Gestisce la registrazione."""
		username = self.username_entry.get()
		password = self.password_entry.get()
		role = self.role_combobox.get()
		data_nascita = self.data_nascita_entry.get()

		if not username or not password or not data_nascita:
			messagebox.showerror("Errore", "Tutti i campi sono obbligatori!")
			return

		try:
			giorno, mese, anno = map(int, data_nascita.split("/"))
			import datetime
			datetime.date(anno, mese, giorno)
		except ValueError:
			messagebox.showerror("Errore", "Inserire una data di nascita valida nel formato DD/MM/YYYY!")
			return

		if save_user(username, password, role, data_nascita):
			messagebox.showinfo("Successo", "Registrazione completata!")
			if role == "Paziente":
				self.app.open_area_paziente(username, data_nascita)
			elif role == "Gestore":
				self.app.open_area_gestore(username)
			self.root.destroy()
		else:
			messagebox.showerror("Errore", "L'utente esiste già!")

	def get_role(self, username, password):
		"""Ottieni il ruolo dell'utente dopo il login."""
		return validate_user(username, password)
