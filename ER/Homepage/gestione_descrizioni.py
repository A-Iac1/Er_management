import json
import os
import customtkinter as ctk

# Definisci la cartella dati e il percorso del file JSON in modo relativo
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Directory corrente del file
DATA_DIR = os.path.join(BASE_DIR, "dati")  # Cartella 'dati'
FILE_DESCRIZIONI = os.path.join(DATA_DIR, "descrizione.json")  # Percorso completo del file 'descrizione.json'

# Funzione per caricare le descrizioni dei pazienti da un file JSON
def carica_descrizioni():
    if not os.path.exists(FILE_DESCRIZIONI):
        return {}
    with open(FILE_DESCRIZIONI, "r") as file:
        return json.load(file)

# Funzione per salvare una descrizione per un paziente nel file JSON
def salva_descrizione(paziente_id, descrizione):
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)  # Crea la cartella 'dati' se non esiste

    descrizioni = carica_descrizioni()
    descrizioni[paziente_id] = descrizione
    with open(FILE_DESCRIZIONI, "w") as file:
        json.dump(descrizioni, file, indent=4)

# Funzione per ottenere la descrizione di un paziente
def ottieni_descrizione(paziente_id):
    descrizioni = carica_descrizioni()
    return descrizioni.get(paziente_id, "")

# Funzione per aprire la finestra di modifica della descrizione
def modifica_descrizione_finestra(root, paziente_id):
    descrizione_corrente = ottieni_descrizione(paziente_id)

    def salva():
        nuova_descrizione = text_area.get("1.0", "end-1c")
        salva_descrizione(paziente_id, nuova_descrizione)
        window.destroy()

    window = ctk.CTkToplevel(root)
    window.title(f"Modifica Descrizione Paziente {paziente_id}")
    window.geometry("400x300")

    label = ctk.CTkLabel(window, text=f"Descrizione del Paziente {paziente_id}")
    label.pack(pady=10)

    text_area = ctk.CTkTextbox(window, width=350, height=150)
    text_area.insert("1.0", descrizione_corrente)
    text_area.pack(pady=10)

    salva_button = ctk.CTkButton(window, text="Salva Descrizione", command=salva)
    salva_button.pack(pady=10)
