from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Funzione per connettersi al database
def get_db_connection():
    conn = sqlite3.connect('iscrizioni_evento.db')
    conn.row_factory = sqlite3.Row
    return conn

# Rotta per la homepage e form di iscrizione
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("INSERT INTO iscrizioni (nome, email) VALUES (?, ?)", (nome, email))
            conn.commit()
            conn.close()
            return redirect(url_for('iscrizioni'))
        except sqlite3.IntegrityError:
            conn.close()
            return "Errore: l'email inserita è già registrata."

    return render_template('index.html')

# Rotta per visualizzare tutte le iscrizioni
@app.route('/iscrizioni')
def iscrizioni():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM iscrizioni")
    iscrizioni = cursor.fetchall()
    conn.close()
    return render_template('iscrizioni.html', iscrizioni=iscrizioni)

# Funzione per creare la tabella nel database se non esiste
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS iscrizioni (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE
    )
    ''')
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()  # Inizializza il database
    app.run(debug=True)
