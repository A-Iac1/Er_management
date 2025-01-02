import customtkinter as ctk
from tkinter import messagebox, ttk  # Aggiungi ttk per Treeview
from tkcalendar import Calendar
import json
import os
from paziente import aggiungi_paziente  # Importa la funzione aggiungi_paziente

# Percorsi dei file JSON
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "dati")
FILE_DOTTORI = os.path.join(DATA_DIR, "dottori.json")
FILE_PAZIENTI = os.path.join(DATA_DIR, "pazienti.json")

# Crea la cartella "dati" se non esiste
os.makedirs(DATA_DIR, exist_ok=True)

# Funzioni di gestione file JSON
def carica_dati(file):
    if not os.path.exists(file):
        return []
    try:
        with open(file, "r", encoding="utf-8") as f:
            return json.load(f) or []
    except json.JSONDecodeError:
        return []


def salva_dati(file, dati):
    with open(file, "w", encoding="utf-8") as f:
        json.dump(dati, f, indent=4)

class AreaPaziente:
    def __init__(self, root, username, data_nascita):
        self.root = root
        self.username = username
        self.data_nascita = data_nascita  # Memorizza la data di nascita
        self.dottori = carica_dati(FILE_DOTTORI)
        self.visite = carica_dati(FILE_PAZIENTI)

        self.root.title(f"Area Paziente - {self.username}")
        self.root.geometry("800x600")

        # Impostiamo il tema scuro
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        # Titolo
        title = ctk.CTkLabel(self.root, text=f"Benvenuto, {self.username}!", font=("Arial", 22, "bold"))
        title.pack(pady=20)

        # Frame principale
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(padx=10, pady=10, fill="both", expand=True)

        # Sezione di ricerca
        search_frame = ctk.CTkFrame(self.main_frame)
        search_frame.pack(pady=10, fill="x")

        lbl_cerca = ctk.CTkLabel(search_frame, text="Cerca dottore:", font=("Arial", 14))
        lbl_cerca.pack(side="left", padx=10)

        self.entry_cerca = ctk.CTkEntry(search_frame, width=150)
        self.entry_cerca.pack(side="left", padx=5)

        lbl_spec = ctk.CTkLabel(search_frame, text="Specializzazione:", font=("Arial", 14))
        lbl_spec.pack(side="left", padx=5)

        # Combobox delle specializzazioni
        self.combo_spec = ctk.CTkComboBox(search_frame, values=[], state="normal", width=150)
        self.combo_spec.pack(side="left", padx=5)
        self.aggiorna_combobox_specializzazioni()

        btn_cerca = ctk.CTkButton(search_frame, text="Cerca", command=self.cerca_dottore)
        btn_cerca.pack(side="left", padx= 50)

        # Tabella dei dottori (usando ttk.Treeview)
        columns = ("ID", "Nome", "Specializzazione")
        self.treeview = ttk.Treeview(self.main_frame, columns=columns, show="headings", height=15)
        self.treeview.pack(pady=10, fill="both", expand=True)

        for col in columns:
            self.treeview.heading(col, text=col)
            self.treeview.column(col, width=150, anchor="center")

        btn_prenota = ctk.CTkButton(self.root, text="Prenota Visita", command=self.prenota_visita)
        btn_prenota.pack(pady=10)

        self.aggiorna_lista_dottori()

    # Funzione per aggiornare la combobox delle specializzazioni
    def aggiorna_combobox_specializzazioni(self):
        specializzazioni = sorted(set(d["Specializzazione"] for d in self.dottori))
        specializzazioni.insert(0, "Tutte")
        self.combo_spec.configure(values=specializzazioni)
        self.combo_spec.set("Tutte")

    # Funzione di ricerca
    def cerca_dottore(self):
        search_term_nome = self.entry_cerca.get().lower()
        search_term_spec = self.combo_spec.get()

        for row in self.treeview.get_children():
            self.treeview.delete(row)

        for dottore in self.dottori:
            if (search_term_nome in dottore["Nome"].lower() or not search_term_nome) and \
               (search_term_spec == "Tutte" or dottore["Specializzazione"] == search_term_spec):
                self.treeview.insert("", "end", values=(dottore["id"], dottore["Nome"], dottore["Specializzazione"]))

    # Funzione per aggiornare la lista dei dottori
    def aggiorna_lista_dottori(self):
        for row in self.treeview.get_children():
            self.treeview.delete(row)
        for dottore in self.dottori:
            self.treeview.insert("", "end", values=(dottore["id"], dottore["Nome"], dottore["Specializzazione"]))

    def apri_calendario(self):
        # Finestra di dialogo per la selezione della data
        def seleziona_data():
            self.data_visita = cal.get_date()  # Ottieni la data selezionata
            finestra_calendario.destroy()  # Chiudi la finestra del calendario

        # Creazione della finestra del calendario
        finestra_calendario = ctk.CTkToplevel()
        finestra_calendario.title("Seleziona Data Visita")
        finestra_calendario.geometry("400x400")
        finestra_calendario.grab_set()  # Disabilita altre finestre finché questa è aperta

        # Widget Calendario
        cal = Calendar(
            finestra_calendario,
            selectmode="day",
            date_pattern="dd/mm/yyyy",  # Formato della data
        )
        cal.pack(pady=20)

        # Bottone per confermare la selezione
        ctk.CTkButton(finestra_calendario, text="Seleziona", command=seleziona_data).pack(pady=10)

        # Aspetta la chiusura della finestra
        finestra_calendario.wait_window()

        # Restituisci la data selezionata
        return self.data_visita

    # Funzione per prenotare una visita
    def prenota_visita(self):
        selected_item = self.treeview.selection()
        if not selected_item:
            messagebox.showerror("Errore", "Seleziona un dottore per prenotare una visita.")
            return

        dottore_id = int(self.treeview.item(selected_item)["values"][0])
        dottore = next((d for d in self.dottori if d["id"] == dottore_id), None)

        if not dottore:
            messagebox.showerror("Errore", "Dottore non trovato.")
            return

        # Apri il calendario per selezionare la data
        self.data_visita = self.apri_calendario()  # Si assume che apri_calendario restituisca una data

        if not self.data_visita:
            messagebox.showerror("Errore", "Data non selezionata.")
            return

        # Aggiungi il paziente con la visita
        entry_nome = self.username  # Nome del paziente (stringa)
        entry_data_nascita = self.data_nascita  # Usa la data di nascita salvata
        entry_visita = self.data_visita  # Usa la data scelta dal calendario
        combo_dottore = dottore["Nome"]  # Nome del dottore (stringa)

        # Chiamata alla funzione aggiungi_paziente
        aggiungi_paziente(entry_nome, entry_data_nascita, entry_visita, combo_dottore, None)  # Passa None al posto di Treeview

        # Mostra un messaggio di successo
        messagebox.showinfo("Successo", "Visita prenotata con successo.")

        # Aggiorna la lista dei dottori
        self.aggiorna_lista_dottori()


# Avvio dell'applicazione
if __name__ == "__main__":
    root = ctk.CTk()
    app = AreaPaziente(root, username="Paziente01", data_nascita="01/01/1990")  
    root.mainloop()
