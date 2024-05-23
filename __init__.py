from flask import Flask, request, render_template, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'votre_clé_secrète'

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/fiche_nom/', methods=['GET', 'POST'])
def fiche_nom():
    if 'user' not in session:
        return redirect(url_for('login_user'))

    if request.method == 'POST':
        nom = request.form['nom']
        conn = get_db_connection()
        client = conn.execute('SELECT * FROM clients WHERE nom = ?', (nom,)).fetchone()
        conn.close()
        if client is None:
            return 'Client non trouvé!'
        return render_template('fiche_nom.html', client=client)
    return render_template('recherche_nom.html')

@app.route('/login_user', methods=['GET', 'POST'])
def login_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'user' and password == '12345':
            session['user'] = username
            return redirect(url_for('fiche_nom'))
        return 'Login échoué!'
    return render_template('login_user.html')

@app.route('/logout_user')
def logout_user():
    session.pop('user', None)
    return redirect(url_for('login_user'))

if __name__ == '__main__':
    app.run(debug=True)
