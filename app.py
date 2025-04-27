from flask import Flask, render_template, request, send_from_directory
import re

app = Flask(__name__)

# Pour servir les fichiers statiques
@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

# Fonction pour nettoyer le code
def nettoyer_code(code_saisi):
    code = code_saisi.strip().upper()

    if len(code) >= 3:
        derniers_3 = code[-3:]

        if '-' in derniers_3:
            position_tiret = derniers_3.index('-')

            # Cas 1 : Lettre A-I avant le tiret
            if position_tiret > 0 and derniers_3[position_tiret - 1] in 'ABCDEFGHI':
                code = code[:-3] + derniers_3[:position_tiret - 1] + derniers_3[position_tiret + 1:]

            # Cas 2 : Lettre A-I après le tiret
            elif position_tiret + 1 < len(derniers_3) and derniers_3[position_tiret + 1] in 'ABCDEFGHI':
                code = code[:-3] + derniers_3[:position_tiret] + derniers_3[position_tiret + 2:]

    # Cas 3 : Si le dernier caractère est une lettre A-I → on l'enlève
    if code and code[-1] in 'ABCDEFGHI':
        code = code[:-1]

    return code

# Fonction pour rechercher un code dans code.txt
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

# Fonction pour générer la réponse
def generer_reponse(code_saisi):
    code_nettoye = nettoyer_code(code_saisi)
    prix, delai = rechercher_code(code_nettoye)
    if prix is None:
        return f"Code : {code_nettoye}<br>Résultat : Aucun résultat trouvé."
    elif prix == "":
        return f"Code : {code_nettoye}<br>Prix : nous consulter<br>Délai : {delai}"
    else:
        return f"Code : {code_nettoye}<br>Prix : {prix}<br>Délai : {delai}"

# Route principale
@app.route('/', methods=['GET', 'POST'])
def index():
    reponse = None
    if request.method == 'POST':
        code_saisi = request.form.get('code')
        if code_saisi:
            reponse = generer_reponse(code_saisi)
    return render_template('index.html', reponse=reponse)

# Lancement du serveur local
if __name__ == "__main__":
    app.run(debug=True)
