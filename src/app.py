from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

# Pfad zur JSON-Datei
json_file_path = os.path.join(os.path.dirname(__file__), 'books_data.json')

# Überprüfe, ob die JSON-Datei existiert, und erstelle sie, falls nicht
if not os.path.exists(json_file_path):
    with open(json_file_path, 'w', encoding='utf-8') as file:
        json.dump([], file)

@app.route('/api/books', methods=['GET'])
def get_books():
    with open(json_file_path, 'r', encoding='utf-8') as file:
        books = json.load(file)
    return jsonify(books)

@app.route('/api/add_book', methods=['POST'])
def add_book():
    data = request.get_json()

    new_book = {
        'title': data['title'],
        'author': data['author'],
        'color': generate_random_color()
    }

    # Lese vorhandene Bücher aus der JSON-Datei
    with open(json_file_path, 'r', encoding='utf-8') as file:
        existing_books = json.load(file)

    # Füge das neue Buch hinzu
    existing_books.append(new_book)

    # Speichere die aktualisierten Bücher in der JSON-Datei
    with open(json_file_path, 'w', encoding='utf-8') as file:
        json.dump(existing_books, file, indent=2)

    return jsonify(new_book)

def generate_random_color():
    # Generiere eine zufällige Hintergrundfarbe
    color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
    return color

if __name__ == '__main__':
    app.run(debug=True)
