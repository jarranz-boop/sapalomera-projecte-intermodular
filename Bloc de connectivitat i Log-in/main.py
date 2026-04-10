import sqlite3
import bcrypt
import tkinter as tk
from tkinter import messagebox
import os

# --- LÒGICA DE BASE DE DADES (Sense canvis) ---
def inicialitzar_bd():
    conn = sqlite3.connect('hospital_montserrat.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash BLOB NOT NULL
        )
    ''')
    conn.commit()
    return conn

def registrar_usuari(usuari, contrasenya):
    if not usuari or not contrasenya:
        messagebox.showwarning("Atenció", "Tots els camps són obligatoris")
        return
    conn = inicialitzar_bd()
    cursor = conn.cursor()
    hash_pw = bcrypt.hashpw(contrasenya.encode('utf-8'), bcrypt.gensalt())
    try:
        cursor.execute('INSERT INTO usuarios (username, password_hash) VALUES (?, ?)', (usuari, hash_pw))
        conn.commit()
        messagebox.showinfo("Èxit", f"Usuari '{usuari}' registrat correctament.")
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Aquest nom d'usuari ja existeix.")
    finally:
        conn.close()

def validar_login(usuari, contrasenya):
    conn = inicialitzar_bd()
    cursor = conn.cursor()
    cursor.execute('SELECT password_hash FROM usuarios WHERE username = ?', (usuari,))
    resultat = cursor.fetchone()
    conn.close()
    if resultat and bcrypt.checkpw(contrasenya.encode('utf-8'), resultat[0]):
        messagebox.showinfo("Accés Concedit", f"Benvingut, {usuari}")
    else:
        messagebox.showerror("Error", "Usuari o contrasenya incorrectes")

# --- INTERFAZ GRÀFICA MILLORADA ---

class AplicacioHospital:
    def __init__(self, root):
        self.root = root
        self.root.title("Hospital Montserrat - Gestió d'Accés")
        
        # --- PALETA DE COLORS EXTRARETA DEL LOGO ---
        self.color_blau_fosc = "#2b56cc"  # Blau del contorn
        self.color_blau_clar = "#00d4ff"  # Cian de l'interior
        self.color_blanc = "#ffffff"
        self.color_gris_text = "#444444"

        self.root.configure(bg=self.color_blanc)
        self.root.geometry("450x550") # Mida ideal
        self.root.resizable(False, False)

        # --- CARREGA I REDIMENSIÓ DEL LOGO ---
        ruta_script = os.path.dirname(os.path.abspath(__file__))
        ruta_logo = os.path.join(ruta_script, "images", "Hospital-Montserrat_Logo.png")

        try:
            img_original = tk.PhotoImage(file=ruta_logo)
            # Redimensionem: subsample divideix la mida. 
            # Si la imatge és molt gran, prova amb (4, 4) o (6, 6)
            self.logo = img_original.subsample(5, 5) 
            
            self.lbl_logo = tk.Label(root, image=self.logo, bg=self.color_blanc)
            self.lbl_logo.pack(pady=20)
        except Exception as e:
            print(f"Error amb el logo: {e}")
            tk.Label(root, text="HOSPITAL\nMONTSERRAT", font=("Segoe UI", 24, "bold"), 
                     fg=self.color_blau_fosc, bg=self.color_blanc).pack(pady=20)

        # --- FORMULARI ---
        main_frame = tk.Frame(root, bg=self.color_blanc)
        main_frame.pack(pady=10, padx=50, fill="both")

        # Usuari
        tk.Label(main_frame, text="Nom d'usuari", font=("Segoe UI", 10, "bold"), 
                 bg=self.color_blanc, fg=self.color_gris_text).pack(anchor="w")
        self.entry_user = tk.Entry(main_frame, font=("Segoe UI", 12), bd=2, relief="flat", highlightthickness=1)
        self.entry_user.config(highlightbackground="#cccccc", highlightcolor=self.color_blau_clar)
        self.entry_user.pack(fill="x", pady=(5, 15))

        # Contrasenya
        tk.Label(main_frame, text="Contrasenya", font=("Segoe UI", 10, "bold"), 
                 bg=self.color_blanc, fg=self.color_gris_text).pack(anchor="w")
        self.entry_pw = tk.Entry(main_frame, font=("Segoe UI", 12), show="*", bd=2, relief="flat", highlightthickness=1)
        self.entry_pw.config(highlightbackground="#cccccc", highlightcolor=self.color_blau_clar)
        self.entry_pw.pack(fill="x", pady=(5, 20))

        # --- BOTONS AMB ESTIL ---
        self.btn_login = tk.Button(main_frame, text="INICIAR SESSIÓ", font=("Segoe UI", 11, "bold"),
                                   bg=self.color_blau_fosc, fg="white", cursor="hand2",
                                   activebackground=self.color_blau_clar, activeforeground="white",
                                   relief="flat", command=self.executar_login, pady=10)
        self.btn_login.pack(fill="x", pady=5)

        self.btn_reg = tk.Button(main_frame, text="Enregistrar nou usuari", font=("Segoe UI", 10),
                                 bg=self.color_blanc, fg=self.color_blau_fosc, cursor="hand2",
                                 relief="flat", command=self.executar_registre)
        self.btn_reg.pack(fill="x")

    def executar_login(self):
        validar_login(self.entry_user.get(), self.entry_pw.get())

    def executar_registre(self):
        registrar_usuari(self.entry_user.get(), self.entry_pw.get())

if __name__ == "__main__":
    root = tk.Tk()
    app = AplicacioHospital(root)
    root.mainloop()