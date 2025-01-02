import json
import os
import bcrypt

# Percorsi per i file e le cartelle
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Account_Gestore
DATA_DIR = os.path.join(BASE_DIR, "dati")  # Cartella 'dati'
USER_FILE = os.path.join(DATA_DIR, "users.json")  # File 'users.json' nella cartella 'dati'

def ensure_data_directory():
    """Assicurati che la cartella 'dati' esista, altrimenti creala."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

def load_users():
    """Carica gli utenti dal file JSON e assicurati che sia un dizionario."""
    ensure_data_directory()  # Verifica che la cartella esista

    # Se il file users.json non esiste, restituisci un dizionario vuoto
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as f:
            try:
                users = json.load(f)
                if isinstance(users, dict):  # Assicurati che i dati siano un dizionario
                    return users
                else:
                    return {}  # Restituisci un dizionario vuoto se i dati non sono corretti
            except json.JSONDecodeError:
                return {}  # Se il JSON è malformato, ritorna un dizionario vuoto
    return {}

def save_user(username, password, role, data_nascita):
    """Salva un nuovo utente con il ruolo e la data di nascita nel file JSON, hashando la password."""
    users = load_users()
    
    # Se l'utente esiste già, restituisce False
    if username in users:
        return False
    
    # Hash della password con bcrypt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Salva il nuovo utente con i dettagli aggiuntivi
    users[username] = {
        "password": hashed_password.decode('utf-8'),
        "role": role,
        "data_nascita": data_nascita  # Aggiunto il campo data di nascita
    }
    
    # Scrive gli utenti nel file JSON
    with open(USER_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=4, ensure_ascii=False)  # Usa ensure_ascii=False per supportare caratteri speciali

    return True


def validate_user(username, password):
    """Verifica le credenziali dell'utente."""
    users = load_users()  # Supponiamo che 'load_users' carichi gli utenti da un file o database

    if username in users:
        user = users[username]
        if bcrypt.checkpw(password.encode('utf-8'), user["password"].encode('utf-8')):
            role = user["role"]
            data_nascita = user.get("data_nascita", "Non Specificato")  # Aggiungi la data di nascita
            return role, data_nascita  # Restituisci anche la data di nascita
    return None, None  # Se non trovate le credenziali, restituisci None

