from flask import Flask, request, render_template, redirect, url_for, flash
import yt_dlp
import os
import secrets

app = Flask(__name__)

# Génération d'une clé secrète aléatoire
app.secret_key = secrets.token_hex(16)  # Clé secrète pour signer les cookies et les sessions

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        save_path = request.form['save_path']
        
        if not os.path.isdir(save_path):
            flash('Le chemin du dossier est invalide ou n\'existe pas.')
            return redirect(url_for('index'))

        try:
            download_youtube_video(url, save_path)
            return redirect(url_for('completed'))
        except Exception as e:
            flash(f'Une erreur est survenue : {e}')
            return redirect(url_for('index'))
    return render_template('index.html')

@app.route('/completed')
def completed():
    return render_template('completed.html')

def download_youtube_video(url, save_path):
    try:
        ydl_opts = {
            'format': 'bestvideo[ext=mp4][height<=1440]+bestaudio[ext=m4a]/best[ext=mp4][height<=1440]',
            'outtmpl': os.path.join(save_path, '%(title)s.%(ext)s'),
            'merge_output_format': 'mp4',
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.extract_info(url, download=True)
    except Exception as e:
        print(f'An error occurred: {e}')
        raise

if __name__ == '__main__':
    app.run(debug=True)
