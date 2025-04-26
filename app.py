
from flask import Flask, render_template, request, send_from_directory

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    # ton code ici
    return render_template('index.html')

# Pour servir les fichiers dans /static
@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

def nettoyer_code(code_saisi):
    code = code_saisi.strip().upper()
    if len(code) >= 3:
        dernier_3 = code[-3:]
        if dernier_3[-2] == '-':
            code = code[:-3] + code[-1]
        elif code[-1] in 'ABCDEFGHIJK':
            code = code[:-1]
    return code

def rechercher_code(code_nettoye, fichier_table="code.txt"):
    try:
        with open(fichier_table, 'r', encoding='utf-8-sig') as f:
            lignes = f.readlines()
        for ligne in lignes:
            elements = ligne.strip().split(';')
            if len(elements) >= 3:
                code_table, prix, delai = elements[0].strip().upper(), elements[1].strip(), elements[2].strip()
                if code_nettoye == code_table:
                    return prix, delai
        return None, None
    except FileNotFoundError:
        return None, None

def generer_reponse(code_saisi):
    code_nettoye = nettoyer_code(code_saisi)
    prix, delai = rechercher_code(code_nettoye)
    if prix is None:
        return f"Code : {code_nettoye}\nRésultat : Aucun résultat trouvé."
    elif prix == "":
        return f"Code : {code_nettoye}\nPrix : nous consulter\nDélai : {delai}"
    else:
        return f"Code : {code_nettoye}\nPrix : {prix}\nDélai : {delai}"

@app.route('/', methods=['GET', 'POST'])
def index():
    reponse = None
    if request.method == 'POST':
        code_saisi = request.form.get('code')
        if code_saisi:
            reponse = generer_reponse(code_saisi)
    return render_template('index.html', reponse=reponse)

if __name__ == "__main__":
    app.run(debug=True)
