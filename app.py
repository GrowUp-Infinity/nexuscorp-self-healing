 #Ce fichier contient la logique métier et les failles backend
# 10 failles que nous intégrons 
" Injection SQL (SQLi) : Recherche d'employés non sécurisée"
"Command Injection : Outil de diagnostic réseau (ping) qui exécute des commandes système "
"Path Traversal (LFI) :Consultation de rapports PDF sans vérification de chemin. "
" Insecure Deserialization : Utilisation de la bibliothèque pickle pour charger des préférences utilisateurs. "
"Broken Access Control (IDOR) : Accès aux profils via /user/<id> sans vérification de session."
"Hardcoded Secrets : Clés API AWS et Database codées en dur dans le code. "
" Cross-Site Scripting (XSS) : Affichage du nom d'utilisateur sans échappement HTML"
"Information Exposure : Mode Debug=True activé et route /env exposant les variables"
"SCA (Vulnerable Dependencies) : Utilisation de vieilles versions de Flask/Requests "
" Insecure Docker Config : Application tournant en root dans le conteneur"


 
import os, sqlite3, subprocess, pickle, base64
from flask import Flask, request, render_template, jsonify, render_template_string

app = Flask(__name__)

# FAILLE 8: Mode Debug activé (Exposition d'infos)
app.config['DEBUG'] = True
# FAILLE 6: Secrets codés en dur
AWS_ACCESS_KEY = "AKIA-NEXUS-CORP-5566778899"

def init_db():
    conn = sqlite3.connect('nexus.db')
    conn.execute('CREATE TABLE IF NOT EXISTS staff (id INTEGER PRIMARY KEY, name TEXT, role TEXT, salary TEXT)')
    conn.execute("INSERT OR IGNORE INTO staff VALUES (1, 'Boss', 'CEO', '15000€')")
    conn.execute("INSERT OR IGNORE INTO staff VALUES (2, 'Alice', 'Dev', '4000€')")
    conn.commit()

@app.route('/')
def index():
    # FAILLE 7: XSS via le paramètre 'user'
    user = request.args.get('user', 'Invité')
    return render_template('index.html', user=user)

# FAILLE 1: SQL Injection
@app.route('/api/staff/search')
def search_staff():
    name = request.args.get('name', '')
    conn = sqlite3.connect('nexus.db')
    query = f"SELECT * FROM staff WHERE name = '{name}'" # Danger
    res = conn.execute(query).fetchall()
    return jsonify(res)

# FAILLE 2: Command Injection
@app.route('/api/network/ping')
def network_ping():
    host = request.args.get('host', '127.0.0.1')
    # Danger: shell=True + concatenation
    output = subprocess.check_output(f"ping -c 1 {host}", shell=True).decode()
    return jsonify({"output": output})

# FAILLE 3: Path Traversal
@app.route('/api/reports/view')
def view_report():
    file = request.args.get('file', 'daily.txt')
    path = os.path.join("./reports/", file)
    with open(path, 'r') as f:
        return f.read()

# FAILLE 4: Deserialization
@app.route('/api/prefs/load')
def load_prefs():
    data = request.args.get('data')
    # Danger: pickle.loads est une porte dérobée RCE
    prefs = pickle.loads(base64.b64decode(data))
    return f"Préférences chargées: {prefs}"

# FAILLE 5: IDOR
@app.route('/user/<int:user_id>')
def get_user_profile(user_id):
    # Aucune vérification si l'utilisateur connecté est bien le user_id
    return f"Données privées de l'utilisateur {user_id}"

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)