import json
import os
from tkinter import messagebox
import matplotlib.pyplot as plt

# Percorso del file JSON
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Account_Gestore
DATA_DIR = os.path.join(BASE_DIR, "dati")
FILE_FINANZE = os.path.join(DATA_DIR, "finanze.json")

# Crea la cartella "dati" se non esiste
os.makedirs(DATA_DIR, exist_ok=True)

# Carica le finanze dal file JSON
def carica_dati():
    if not os.path.exists(FILE_FINANZE):
        return []
    try:
        with open(FILE_FINANZE, "r", encoding="utf-8") as f:
            finanze = json.load(f) or []
        return finanze
    except json.JSONDecodeError:
        return []

# Salva le finanze nel file JSON
def salva_dati(finanze):
    with open(FILE_FINANZE, "w", encoding="utf-8") as f:
        json.dump(finanze, f, indent=4)

# Lista iniziale delle finanze
finanze = carica_dati()

# Aggiungi transazione
def aggiungi_transazione(entry_descrizione, entry_importo, entry_tipo, treeview):
    descrizione = entry_descrizione.get()
    importo = entry_importo.get()
    tipo = entry_tipo.get()
    
    if not descrizione or not importo or not tipo:
        messagebox.showerror("Errore", "Compilare tutti i campi.")
        return

    try:
        importo = float(importo)
    except ValueError:
        messagebox.showerror("Errore", "Inserire un importo valido.")
        return

    transazione_id = len(finanze)  # Nuovo ID univoco
    transazione = {"id": transazione_id, "Descrizione": descrizione, "Importo": importo, "Tipo": tipo}
    finanze.append(transazione)
    salva_dati(finanze)
    aggiorna_lista_finanze(treeview)
    messagebox.showinfo("Successo", "Transazione aggiunta correttamente.")

# Elimina transazione
def elimina_transazione(treeview):
    selected_items = treeview.selection()
    if not selected_items:
        messagebox.showerror("Errore", "Seleziona una transazione per eliminarla.")
        return

    for item in selected_items:
        transazione_id = int(treeview.item(item)["values"][0])  # ID della transazione
        finanze[:] = [t for t in finanze if t["id"] != transazione_id]  # Rimuove la transazione
    salva_dati(finanze)
    aggiorna_lista_finanze(treeview)
    messagebox.showinfo("Successo", "Transazioni eliminate correttamente.")

# Aggiorna lista transazioni
def aggiorna_lista_finanze(treeview):
    for row in treeview.get_children():
        treeview.delete(row)
    for transazione in finanze:
        treeview.insert("", "end", values=(transazione["id"], transazione["Descrizione"], transazione["Importo"], transazione["Tipo"]))

def mostra_grafico():
    entrate = sum([t["Importo"] for t in finanze if t["Tipo"] == "Entrata"])
    uscite = sum([t["Importo"] for t in finanze if t["Tipo"] == "Uscita"])

    # Dati per il grafico
    labels = ["Entrate", "Uscite"]
    values = [entrate, uscite]

    # Creazione del grafico a barre
    plt.bar(labels, values, color=["green", "red"])
    plt.title("Grafico Entrate vs Uscite")
    plt.xlabel("Tipo")
    plt.ylabel("Importo (€)")
    plt.show()
    