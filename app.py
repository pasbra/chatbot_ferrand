import os
from flask import Flask, render_template, request, send_from_directory

app = Flask(__name__)

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

def nettoyer_code(code_saisi):
    code = code_saisi.strip().upper()
    if len(code) >= 3:
        derniers_3 = code[-3:]
        if '-' in derniers_3:
            position_tiret = derniers_3.index('-')
            if position_tiret > 0 and derniers_3[position_tiret - 1] in 'ABCDEFGHI':
                code = code[:-3] + derniers_3[:position_tiret - 1] + derniers_3[position_tiret + 1:]
            elif position_tiret + 1 < len(derniers_3) and derniers_3[position_tiret + 1] in 'ABCDEFGHI':
                code = code[:-3] + derniers_3[:position_tiret] + derniers_3[position_tiret + 2:]
    if code and code[-1] in 'ABCDEFGHI':
        code = code[:-1]
    return code

def rechercher_code(code_nettoye, fichier_table="code.txt"):
    fichier_table = os.path.join(app.root_path, fichier_table)
    try:
        with open(fichier_table, 'r', encoding='cp1252') as f:
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
        return f"Code : {code_nettoye}<br>Résultat : Aucun résultat trouvé."
    elif prix == "":
        return f"Code : {code_nettoye}<br>Prix : nous consulter<br>Délai : {delai}"
    else:
        return f"Code : {code_nettoye}<br>Prix : {prix}<br>Délai : {delai}"

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
