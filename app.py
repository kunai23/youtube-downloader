from flask import Flask, request, redirect, url_for, render_template, flash
from pytube import YouTube
import os
import psutil
import secrets
import yt_dlp

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
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
