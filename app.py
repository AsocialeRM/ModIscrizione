from functools import wraps
from flask import session

app.secret_key = 'chiave_super_segretissima'  # Cambiala in qualcosa di sicuro

# Credenziali admin (puoi cambiarle)
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'admin'



def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('registro'))
        else:
            error = 'Credenziali errate'
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))





# app.py
from flask import Flask, render_template, request, redirect, url_for, send_file
import sqlite3
import qrcode
from reportlab.pdfgen import canvas
from datetime import datetime

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    # Tabella iscritti aggiornata
    c.execute('''
        CREATE TABLE IF NOT EXISTS iscritti (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            cognome TEXT NOT NULL,
            luogo_nascita TEXT NOT NULL,
            data_nascita TEXT NOT NULL,
            indirizzo TEXT NOT NULL,
            cap TEXT NOT NULL,
            telefono TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            data_registrazione TEXT NOT NULL,
            consenso INTEGER NOT NULL,
            attivo INTEGER DEFAULT 1,
            anno_2023 INTEGER DEFAULT 0,
            anno_2024 INTEGER DEFAULT 0,
            anno_2025 INTEGER DEFAULT 0
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS presenze (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            iscritto_id INTEGER,
            data_ora TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

@app.route('')
def ASOCIALE():
    return render_template('ASOCIALE.html')

@app.route('verifica', methods=['POST'])
def verifica():
    contatto = request.form['contatto']
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        SELECT  FROM iscritti WHERE (email =  OR telefono = ) AND attivo = 1
    ''', (contatto, contatto))
    risultato = c.fetchone()
    conn.close()

    if risultato
        # Se trovato, mostro i dati
        return render_template('dati_esistenti.html', iscritto=risultato)
    else
        # Se non trovato, vado al modulo iscrizione
        return render_template('iscrizione.html')

@app.route('nuova_iscrizione', methods=['POST'])
def nuova_iscrizione():
    nome = request.form['nome']
    cognome = request.form['cognome']
    luogo_nascita = request.form['luogo_nascita']
    data_nascita = request.form['data_nascita']
    indirizzo = request.form['indirizzo']
    cap = request.form['cap']
    telefono = request.form['telefono']
    email = request.form['email']
    consenso = int(request.form.get('consenso', 0))

    data_registrazione = datetime.now().strftime(%Y-%m-%d)

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO iscritti 
        (nome, cognome, luogo_nascita, data_nascita, indirizzo, cap, telefono, email, data_registrazione, consenso, attivo)
        VALUES (, , , , , , , , , , 1)
    ''', (nome, cognome, luogo_nascita, data_nascita, indirizzo, cap, telefono, email, data_registrazione, consenso))
    iscritto_id = c.lastrowid
    conn.commit()
    conn.close()

    # Genera QR code con ID iscritto
    qr = qrcode.make(str(iscritto_id))
    qr_path = f'tessereqr_{iscritto_id}.png'
    qr.save(qr_path)

    # Genera PDF tessera
    pdf_path = f'tesseretessera_{iscritto_id}.pdf'
    c = canvas.Canvas(pdf_path)
    c.drawString(100, 750, fNome {nome})
    c.drawString(100, 730, fCognome {cognome})
    c.drawString(100, 710, fID Iscritto {iscritto_id})
    c.drawImage(qr_path, 100, 600, width=100, height=100)
    c.save()

    return render_template('success.html', pdf_path=pdf_path)

@app.route('downloadpathfilename')
def download(filename):
    return send_file(filename, as_attachment=True)

if __name__ == '__main__'
    init_db()
    app.run(debug=True)


@app.route('/registro')
@login_required
def registro():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT * FROM iscritti')
    iscritti = c.fetchall()
    conn.close()
    return render_template('registro.html', iscritti=iscritti)

@app.route('/aggiorna_registro', methods=['POST'])
@login_required
def aggiorna_registro():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Prendo tutti gli iscritti per aggiornare i loro valori
    c.execute('SELECT id FROM iscritti')
    iscritti = c.fetchall()

    for iscritto in iscritti:
        iscritto_id = iscritto[0]

        attivo = 1 if request.form.get(f'attivo_{iscritto_id}') == 'on' else 0
        anno_2023 = 1 if request.form.get(f'anno_2023_{iscritto_id}') == 'on' else 0
        anno_2024 = 1 if request.form.get(f'anno_2024_{iscritto_id}') == 'on' else 0
        anno_2025 = 1 if request.form.get(f'anno_2025_{iscritto_id}') == 'on' else 0

        c.execute('''
            UPDATE iscritti SET attivo = ?, anno_2023 = ?, anno_2024 = ?, anno_2025 = ? WHERE id = ?
        ''', (attivo, anno_2023, anno_2024, anno_2025, iscritto_id))

    conn.commit()
    conn.close()
    return redirect(url_for('registro'))




@app.route('/presenza/<int:iscritto_id>')
def registra_presenza(iscritto_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Recupero dati iscritto
    c.execute('SELECT * FROM iscritti WHERE id = ?', (iscritto_id,))
    iscritto = c.fetchone()

    # Controllo se già registrato oggi
    oggi = datetime.now().strftime("%Y-%m-%d")
    c.execute('''
        SELECT * FROM presenze 
        WHERE iscritto_id = ? AND date(data_ora) = ?
    ''', (iscritto_id, oggi))
    presenza = c.fetchone()

    if not presenza:
        # Se non ancora registrato oggi, registro presenza
        c.execute('INSERT INTO presenze (iscritto_id) VALUES (?)', (iscritto_id,))
        conn.commit()

    conn.close()

    return render_template('presenza_registrata.html', iscritto=iscritto, registrata=not presenza)



@app.route('/presenze_oggi')
@login_required
def presenze_oggi():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    oggi = datetime.now().strftime("%Y-%m-%d")
    c.execute('''
        SELECT iscritti.nome, iscritti.cognome, iscritti.email, presenze.data_ora
        FROM presenze
        JOIN iscritti ON presenze.iscritto_id = iscritti.id
        WHERE date(presenze.data_ora) = ?
    ''', (oggi,))
    presenze = c.fetchall()
    conn.close()

    return render_template('presenze_oggi.html', presenze=presenze)


