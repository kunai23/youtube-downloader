from flask import Flask, request, redirect, url_for, render_template
from pytube import YouTube
import os
import psutil
import secrets

app = Flask(__name__)

# Utiliser une clé secrète par défaut ou définie via une variable d'environnement
app.secret_key = os.getenv('SECRET_KEY', secrets.token_hex(16))

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        save_path = request.form['save_path']
        try:
            yt = YouTube(url)
            video = yt.streams.get_highest_resolution()
            video.download(output_path=save_path)
            return redirect(url_for('completed'))
        except Exception as e:
            return f"Une erreur est survenue : {str(e)}", 500

    return render_template('index.html')

@app.route('/completed')
def completed():
    return render_template('completed.html')

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
