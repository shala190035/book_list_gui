from flask import Flask, render_template, request, redirect
from tinydb import TinyDB
import json
import os
import random

app = Flask(__name__)

# TinyDB-Konfiguration
db = TinyDB('data.json')  # Die Datenbank wird in einer JSON-Datei gespeichert

# Zufällige Hintergrundfarbe generieren
def generate_random_color():
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))

# Definition des field_mapping
field_mapping = {
    "Titel": "title",
    " Autor": "author",
    " Veroeffentlichungsjahr": "year",
    " Genre": "genre"
}

# Funktion zum Konvertieren von JSON-Daten in die erwartete Struktur
def convert_to_expected_structure(json_data):
    converted_data = []
    for item in json_data:
        converted_item = {}
        for old_key, new_key in field_mapping.items():
            if old_key in item:  # Überprüfen, ob das alte Schlüsselwort vorhanden ist
                converted_item[new_key] = item[old_key]
        converted_item["color"] = generate_random_color()
        converted_data.append(converted_item)
    return converted_data

# Routing für die Hauptseite
@app.route('/')
def index():
    data = db.all()
    return render_template('index.html', books=data)

# Routing für den Upload der JSON-Datei
@app.route('/upload', methods=['POST'])
def upload():
    # Überprüfen, ob eine Datei hochgeladen wurde
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']

    # Überprüfen, ob die Datei vorhanden und eine JSON-Datei ist
    if file.filename == '' or not file.filename.endswith('.json'):
        return redirect(request.url)

    # JSON-Daten aus der hochgeladenen Datei lesen
    json_data = json.load(file)

    # Konvertieren der JSON-Daten in die erwartete Struktur
    converted_data = convert_to_expected_structure(json_data)

    # Daten in TinyDB speichern
    db.insert_multiple(converted_data)

    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
