import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

# Percorso del file JSON
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Account_Gestore
DATA_DIR = os.path.join(BASE_DIR, "dati")
FILE_DOTTORI = os.path.join(DATA_DIR, "dottori.json")

# Crea la cartella "dati" se non esiste
os.makedirs(DATA_DIR, exist_ok=True)

# Carica le finanze dal file JSON
def carica_dati():
    if not os.path.exists(FILE_DOTTORI):
        return []
    try:
        with open(FILE_DOTTORI, "r", encoding="utf-8") as f:
            dottori = json.load(f) or []
        return dottori
    except json.JSONDecodeError:
        return []

# Salva le finanze nel file JSON
def salva_dati(dottori):
    with open(FILE_DOTTORI, "w", encoding="utf-8") as f:
        json.dump(dottori, f, indent=4)

# Lista iniziale dei dottori
dottori = carica_dati()

# Aggiungi dottore
def aggiungi_dottore(entry_nome, entry_specializzazione, treeview):
    nome = entry_nome.get()
    specializzazione = entry_specializzazione.get()
    
    if not nome or not specializzazione:
        messagebox.showerror("Errore", "Compilare tutti i campi.")
        return

    dottore_id = len(dottori)  # Nuovo ID univoco
    dottore = {
        "id": dottore_id, 
        "Nome": nome, 
        "Specializzazione": specializzazione,
    }
    dottori.append(dottore)
    salva_dati(dottori)
    aggiorna_lista_dottori(treeview)
    messagebox.showinfo("Successo", "Dottore aggiunto correttamente.")

# Elimina dottore
def elimina_dottore(treeview):
    selected_items = treeview.selection()
    if not selected_items:
        messagebox.showerror("Errore", "Seleziona almeno un dottore per eliminarlo.")
        return

    for item in selected_items:
        dottore_id = int(treeview.item(item)["values"][0])  # ID dottore
        dottori[:] = [d for d in dottori if d["id"] != dottore_id]  # Rimuove il dottore
    salva_dati(dottori)
    aggiorna_lista_dottori(treeview)
    messagebox.showinfo("Successo", "Dottori eliminati correttamente.")

# Modifica dottore
def modifica_dottore(treeview, entry_nome, entry_specializzazione):
    selected_item = treeview.selection()
    if not selected_item:
        messagebox.showerror("Errore", "Seleziona un dottore per modificarlo.")
        return
    
    dottore_id = int(treeview.item(selected_item)["values"][0])  # ID dottore
    dottore = next((d for d in dottori if d["id"] == dottore_id), None)
    
    if dottore:
        nome = entry_nome.get()
        specializzazione = entry_specializzazione.get()
        
        if not nome or not specializzazione:
            messagebox.showerror("Errore", "Compilare tutti i campi.")
            return

        dottore["Nome"] = nome
        dottore["Specializzazione"] = specializzazione
        
        salva_dati(dottori)
        aggiorna_lista_dottori(treeview)
        messagebox.showinfo("Successo", "Dottore aggiornato correttamente.")

# Aggiorna lista dottori
def aggiorna_lista_dottori(treeview):
    for row in treeview.get_children():
        treeview.delete(row)
    for dottore in dottori:
        treeview.insert("", "end", values=(dottore["id"], dottore["Nome"], dottore["Specializzazione"]))

# Cerca dottore
def cerca_dottore(entry, treeview):
    search_term = entry.get().lower()
    for row in treeview.get_children():
        treeview.delete(row)
    for dottore in dottori:
        if search_term in dottore["Nome"].lower():
            treeview.insert("", "end", values=(dottore["id"], dottore["Nome"], dottore["Specializzazione"]))
