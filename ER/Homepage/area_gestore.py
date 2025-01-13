import customtkinter as ctk
from tkinter import ttk
from paziente import aggiungi_paziente, elimina_paziente, modifica_paziente, cerca_paziente, aggiorna_lista_pazienti, carica_dottori
from risorse_umane import aggiungi_dottore, elimina_dottore, modifica_dottore, cerca_dottore, aggiorna_lista_dottori
from finanze import aggiungi_transazione, elimina_transazione, aggiorna_lista_finanze, mostra_grafico
from gestione_descrizioni import modifica_descrizione_finestra

class AreaGestore:
	def __init__(self, root, username):
		self.root = root
		self.username = username
		self.root.title(f"Area Gestore - {self.username}")
		self.root.geometry("1200x700")

		# Imposta tema scuro o chiaro come nell'applicazione principale
		ctk.set_appearance_mode("dark")  # Usa il tema scuro per l'intera applicazione
		ctk.set_default_color_theme("dark-blue")  # Usa il tema scuro con blu (puoi sostituirlo con il tema desiderato)

		# Titolo
		title = ctk.CTkLabel(self.root, text=f"Benvenuto, {self.username}!", font=("Helvetica", 24, "bold"))
		title.pack(fill="x", pady=10)

		# Barra laterale
		self.sidebar_frame = ctk.CTkFrame(self.root, width=200, height=600, corner_radius=10, fg_color="gray19")  # Colore scuro per la sidebar
		self.sidebar_frame.pack(side="left", fill="y", padx=10)

		# Pulsanti nella barra laterale
		self.btn_flussi = ctk.CTkButton(self.sidebar_frame, text="Gestione Pazienti", command=self.show_flussi, width=180, height=40)
		self.btn_flussi.pack(fill="x", pady=10)

		self.btn_risorse_umane = ctk.CTkButton(self.sidebar_frame, text="Gestione Risorse Umane", command=self.show_risorse_umane, width=180, height=40)
		self.btn_risorse_umane.pack(fill="x", pady=10)

		self.btn_finanze = ctk.CTkButton(self.sidebar_frame, text="Gestione Finanze", command=self.show_risorse_finanziarie, width=180, height=40)
		self.btn_finanze.pack(fill="x", pady=10)

		# Frame principale per il contenuto
		self.main_frame = ctk.CTkFrame(self.root, corner_radius=10, fg_color="gray10")  # Colore scuro per il contenuto principale
		self.main_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

	def clear_main_frame(self):
		"""Pulisce il frame principale per caricare una nuova sezione."""
		for widget in self.main_frame.winfo_children():
			widget.destroy()

	
	def show_flussi(self):
		"""Mostra la sezione per la gestione dei pazienti."""
		self.clear_main_frame()

		title = ctk.CTkLabel(self.main_frame, text="Gestione Pazienti", font=("Helvetica", 22, "bold"))
		title.pack(pady=20)

		# Funzioni di gestione pazienti
		frame_pazienti = ctk.CTkFrame(self.main_frame, fg_color="gray13")  # Colore scuro per il frame pazienti
		frame_pazienti.pack(fill="both", expand=True)

		ctk.CTkLabel(frame_pazienti, text="Cerca Paziente:", text_color="white").pack(pady=5)
		entry_cerca_paziente = ctk.CTkEntry(frame_pazienti)
		entry_cerca_paziente.pack(pady=5)
		ctk.CTkButton(frame_pazienti, text="Cerca", command=lambda: cerca_paziente(entry_cerca_paziente, treeview_pazienti)).pack(pady=5)

		treeview_pazienti = ttk.Treeview(frame_pazienti, columns=("ID", "Nome", "Data di Nascita", "Visita", "Dottore"), show="headings")
		treeview_pazienti.heading("ID", text="ID")
		treeview_pazienti.heading("Nome", text="Nome")
		treeview_pazienti.heading("Data di Nascita", text="Data di Nascita")
		treeview_pazienti.heading("Visita", text="Data Visita")
		treeview_pazienti.heading("Dottore", text="Dottore")
		treeview_pazienti.tag_configure("odd", background="gray25")
		treeview_pazienti.tag_configure("even", background="gray19")
		treeview_pazienti.pack(fill="both", expand=True)

		frame_input_paziente = ctk.CTkFrame(frame_pazienti, fg_color="gray12")  # Colore scuro per il frame input paziente
		frame_input_paziente.pack(pady=10)

		ctk.CTkLabel(frame_input_paziente, text="Nome Paziente:", text_color="white").pack(side="left", padx=5)
		entry_nome = ctk.CTkEntry(frame_input_paziente)
		entry_nome.pack(side="left", padx=5)

		ctk.CTkLabel(frame_input_paziente, text="Data di Nascita:", text_color="white").pack(side="left", padx=5)
		entry_data_nascita = ctk.CTkEntry(frame_input_paziente)
		entry_data_nascita.pack(side="left", padx=5)

		ctk.CTkLabel(frame_input_paziente, text="Data Visita:", text_color="white").pack(side="left", padx=5)
		entry_visita = ctk.CTkEntry(frame_input_paziente)
		entry_visita.pack(side="left", padx=5)

		ctk.CTkLabel(frame_input_paziente, text="Dottore:", text_color="white").pack(side="left", padx=5)
		dottori = carica_dottori()
		combo_dottore = ctk.CTkComboBox(frame_input_paziente, values=[d["Nome"] for d in dottori], state="readonly")
		combo_dottore.pack(side="left", padx=5)

		frame_pazienti_bottoni = ctk.CTkFrame(frame_pazienti, fg_color="gray13")  # Colore scuro per i bottoni
		frame_pazienti_bottoni.pack(pady=10)

		ctk.CTkButton(frame_pazienti_bottoni, text="Aggiungi Paziente", command=lambda: aggiungi_paziente(entry_nome, entry_data_nascita, entry_visita, combo_dottore, treeview_pazienti)).pack(side="left", padx=10)
		ctk.CTkButton(frame_pazienti_bottoni, text="Elimina Paziente", command=lambda: elimina_paziente(treeview_pazienti)).pack(side="left", padx=10)
		ctk.CTkButton(frame_pazienti_bottoni, text="Modifica Paziente", command=lambda: modifica_paziente(treeview_pazienti, entry_nome, entry_data_nascita, entry_visita, combo_dottore)).pack(side="left", padx=10)

		aggiorna_lista_pazienti(treeview_pazienti)

		# Sposta il listener del doppio clic fuori dalla funzione show_flussi
		treeview_pazienti.bind("<Double-1>", lambda event, treeview=treeview_pazienti: self.doppio_clic_paziente(event, treeview))

	def doppio_clic_paziente(self, event, treeview_pazienti):
		item = treeview_pazienti.selection()
		if item:
			paziente_id = treeview_pazienti.item(item[0], "values")[0]  # Prendi l'ID del paziente
			modifica_descrizione_finestra(self.root, paziente_id)
			
	def show_risorse_umane(self):
		"""Mostra la sezione per la gestione delle risorse umane."""
		self.clear_main_frame()

		title = ctk.CTkLabel(self.main_frame, text="Gestione Risorse Umane", font=("Helvetica", 22, "bold"))
		title.pack(pady=20)

		# Funzioni di gestione risorse umane
		frame_dottori = ctk.CTkFrame(self.main_frame, fg_color="gray13")  # Colore scuro per il frame dottori
		frame_dottori.pack(fill="both", expand=True)

		ctk.CTkLabel(frame_dottori, text="Cerca Dottore:", text_color="white").pack(pady=5)
		entry_cerca_dottore = ctk.CTkEntry(frame_dottori)
		entry_cerca_dottore.pack(pady=5)
		ctk.CTkButton(frame_dottori, text="Cerca", command=lambda: cerca_dottore(entry_cerca_dottore, treeview_dottori)).pack(pady=5)

		treeview_dottori = ttk.Treeview(frame_dottori, columns=("ID", "Nome", "Specializzazione"), show="headings")
		treeview_dottori.heading("ID", text="ID")
		treeview_dottori.heading("Nome", text="Nome")
		treeview_dottori.heading("Specializzazione", text="Specializzazione")
		treeview_dottori.tag_configure("odd", background="gray25")
		treeview_dottori.tag_configure("even", background="gray19")
		treeview_dottori.pack(fill="both", expand=True)

		frame_input_dottore = ctk.CTkFrame(frame_dottori, fg_color="gray12")  # Colore scuro per la sezione input dottore
		frame_input_dottore.pack(pady=10)

		ctk.CTkLabel(frame_input_dottore, text="Nome Dottore:", text_color="white").pack(side="left", padx=5)
		entry_nome_dottore = ctk.CTkEntry(frame_input_dottore)
		entry_nome_dottore.pack(side="left", padx=5)

		ctk.CTkLabel(frame_input_dottore, text="Specializzazione:", text_color="white").pack(side="left", padx=5)
		entry_specializzazione = ctk.CTkEntry(frame_input_dottore)
		entry_specializzazione.pack(side="left", padx=5)

		frame_dottori_bottoni = ctk.CTkFrame(frame_dottori, fg_color="gray13")  # Colore scuro per i bottoni
		frame_dottori_bottoni.pack(pady=10)

		ctk.CTkButton(frame_dottori_bottoni, text="Aggiungi Dottore", command=lambda: aggiungi_dottore(entry_nome_dottore, entry_specializzazione, treeview_dottori)).pack(side="left", padx=10)
		ctk.CTkButton(frame_dottori_bottoni, text="Elimina Dottore", command=lambda: elimina_dottore(treeview_dottori)).pack(side="left", padx=10)
		ctk.CTkButton(frame_dottori_bottoni, text="Modifica Dottore", command=lambda: modifica_dottore(treeview_dottori, entry_nome_dottore, entry_specializzazione)).pack(side="left", padx=10)

		aggiorna_lista_dottori(treeview_dottori)

	def show_risorse_finanziarie(self):
		"""Mostra la sezione per la gestione delle finanze."""
		self.clear_main_frame()

		title = ctk.CTkLabel(self.main_frame, text="Gestione Finanze", font=("Helvetica", 22, "bold"))
		title.pack(pady=20)

		# Funzioni di gestione finanze
		frame_finanze = ctk.CTkFrame(self.main_frame, fg_color="gray13")  # Colore scuro per il frame finanze
		frame_finanze.pack(fill="both", expand=True)

		ctk.CTkLabel(frame_finanze, text="Gestione Finanze", text_color="white").pack(pady=5)

		treeview_finanze = ttk.Treeview(frame_finanze, columns=("ID", "Descrizione", "Importo", "Tipo"), show="headings")
		treeview_finanze.heading("ID", text="ID")
		treeview_finanze.heading("Descrizione", text="Descrizione")
		treeview_finanze.heading("Importo", text="Importo (€)")
		treeview_finanze.heading("Tipo", text="Tipo")
		treeview_finanze.tag_configure("odd", background="gray25")
		treeview_finanze.tag_configure("even", background="gray19")
		treeview_finanze.pack(fill="both", expand=True)

		frame_input_finanze = ctk.CTkFrame(frame_finanze, fg_color="gray12")  # Colore scuro per la sezione input finanze
		frame_input_finanze.pack(pady=10)

		ctk.CTkLabel(frame_input_finanze, text="Descrizione:", text_color="white").pack(side="left", padx=5)
		entry_descrizione = ctk.CTkEntry(frame_input_finanze)
		entry_descrizione.pack(side="left", padx=5)

		ctk.CTkLabel(frame_input_finanze, text="Importo (€):", text_color="white").pack(side="left", padx=5)
		entry_importo = ctk.CTkEntry(frame_input_finanze)
		entry_importo.pack(side="left", padx=5)

		ctk.CTkLabel(frame_input_finanze, text="Tipo:", text_color="white").pack(side="left", padx=5)
		entry_tipo = ctk.CTkComboBox(frame_input_finanze, values=["Entrata", "Uscita"], state="readonly")
		entry_tipo.pack(side="left", padx=5)

		frame_finanze_bottoni = ctk.CTkFrame(frame_finanze, fg_color="gray13")  # Colore scuro per i bottoni finanze
		frame_finanze_bottoni.pack(pady=10)

		ctk.CTkButton(frame_finanze_bottoni, text="Aggiungi Transazione", command=lambda: aggiungi_transazione(entry_descrizione, entry_importo, entry_tipo, treeview_finanze)).pack(side="left", padx=10)
		ctk.CTkButton(frame_finanze_bottoni, text="Elimina Transazione", command=lambda: elimina_transazione(treeview_finanze)).pack(side="left", padx=10)

		ctk.CTkButton(frame_finanze_bottoni, text="Mostra Grafico", command=mostra_grafico).pack(side="left", padx=10)

		aggiorna_lista_finanze(treeview_finanze)

# Esempio di avvio dell'area del gestore:
if __name__ == "__main__":
	root = ctk.CTk()
	app = AreaGestore(root, "Gestore01")
	root.mainloop()
