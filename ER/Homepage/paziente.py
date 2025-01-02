import tkinter as tk
import customtkinter as ctk
from tkinter import ttk, messagebox
import json
import os

# Percorso del file JSON
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Account_Gestore
DATA_DIR = os.path.join(BASE_DIR, "dati")
FILE_PAZIENTI = os.path.join(DATA_DIR, "pazienti.json")
FILE_DOTTORI = os.path.join(DATA_DIR, "dottori.json")

# Crea la cartella "dati" se non esiste
os.makedirs(DATA_DIR, exist_ok=True)

# Carica i dati dal file JSON
def carica_dati(file_path):
    if not os.path.exists(file_path):
        return []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f) or []
    except json.JSONDecodeError:
        return []

# Salva i dati nel file JSON
def salva_dati(file_path, dati):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(dati, f, indent=4)

# Lista iniziale dei pazienti
pazienti = carica_dati(FILE_PAZIENTI)

# Ottieni il prossimo ID per i pazienti
def ottieni_prossimo_id():
    if not pazienti:
        return 1  # Se la lista è vuota, l'ID inizia da 1
    return max(p["id"] for p in pazienti) + 1

# Aggiungi paziente
def aggiungi_paziente(entry_nome, entry_data_nascita, entry_visita, combo_dottore, treeview=None):
    nome = entry_nome.get() if isinstance(entry_nome, (tk.Entry, ctk.CTkEntry)) else entry_nome
    data_nascita = entry_data_nascita.get() if isinstance(entry_data_nascita, (tk.Entry, ctk.CTkEntry)) else entry_data_nascita
    visita = entry_visita.get() if isinstance(entry_visita, (tk.Entry, ctk.CTkEntry)) else entry_visita
    # Ottieni solo il valore selezionato dal combobox
    dottore = combo_dottore.get() if isinstance(combo_dottore, ctk.CTkComboBox) else combo_dottore

    # Controllo per campi vuoti
    if not nome or not data_nascita or not visita or not dottore:
        messagebox.showerror("Errore", "Compilare tutti i campi.")
        return

    # Creazione del paziente
    paziente_id = ottieni_prossimo_id()
    paziente = {
        "id": paziente_id,
        "Nome": nome,
        "Data di Nascita": data_nascita,
        "Visita": visita,
        "Dottore": dottore,
    }

    # Aggiungi il paziente alla lista e salva
    pazienti.append(paziente)
    salva_dati(FILE_PAZIENTI, pazienti)

    # Aggiorna il Treeview solo se esiste
    if treeview:
        aggiorna_lista_pazienti(treeview)

    messagebox.showinfo("Successo", "Paziente aggiunto correttamente.")



# Elimina paziente
def elimina_paziente(treeview):
    selected_items = treeview.selection()
    if not selected_items:
        messagebox.showerror("Errore", "Seleziona almeno un paziente per eliminarlo.")
        return

    for item in selected_items:
        paziente_id = int(treeview.item(item)["values"][0])
        pazienti[:] = [p for p in pazienti if p["id"] != paziente_id]
    salva_dati(FILE_PAZIENTI, pazienti)
    aggiorna_lista_pazienti(treeview)
    messagebox.showinfo("Successo", "Pazienti eliminati correttamente.")

# Modifica paziente
def modifica_paziente(treeview, entry_nome, entry_data_nascita, entry_visita, combo_dottore):
    selected_item = treeview.selection()
    if not selected_item:
        messagebox.showerror("Errore", "Seleziona un paziente per modificarlo.")
        return

    paziente_id = int(treeview.item(selected_item)["values"][0])
    paziente = next((p for p in pazienti if p["id"] == paziente_id), None)

    if paziente:
        paziente["Nome"] = entry_nome.get() if isinstance(entry_nome, (tk.Entry, ctk.CTkEntry)) else entry_nome
        paziente["Data di Nascita"] = entry_data_nascita.get() if isinstance(entry_data_nascita, (tk.Entry, ctk.CTkEntry)) else entry_data_nascita
        paziente["Visita"] = entry_visita.get() if isinstance(entry_visita, (tk.Entry, ctk.CTkEntry)) else entry_visita
        paziente["Dottore"] = combo_dottore.get() if isinstance(combo_dottore,ctk.CTkComboBox) else combo_dottore

        if not paziente["Nome"] or not paziente["Data di Nascita"] or not paziente["Visita"]:
            messagebox.showerror("Errore", "Compilare tutti i campi.")
            return

        salva_dati(FILE_PAZIENTI, pazienti)
        aggiorna_lista_pazienti(treeview)
        messagebox.showinfo("Successo", "Paziente aggiornato correttamente.")

# Aggiorna lista pazienti
def aggiorna_lista_pazienti(treeview):
    for row in treeview.get_children():
        treeview.delete(row)
    for paziente in pazienti:
        treeview.insert("", "end", values=(paziente["id"], paziente["Nome"], paziente["Data di Nascita"], paziente["Visita"], paziente["Dottore"]))

# Cerca paziente
def cerca_paziente(entry, treeview):
    search_term = entry.get().lower()
    for row in treeview.get_children():
        treeview.delete(row)
    for paziente in pazienti:
        if search_term in paziente["Nome"].lower():
            treeview.insert("", "end", values=(paziente["id"], paziente["Nome"], paziente["Data di Nascita"], paziente["Visita"], paziente["Dottore"]))

# Carica dottori
def carica_dottori():
    return carica_dati(FILE_DOTTORI)
