from flask import Flask, request, jsonify
import requests
import os
from moviepy.editor import *
from PIL import ImageFont, ImageDraw, Image
import numpy as np
import uuid

app = Flask(__name__)

@app.route('/crear-video', methods=['POST'])
def crear_video():
    data = request.json
    frase = data.get('frase')
    fondo_url = data.get('fondo_url')
    
    # Descargar imagen de fondo
    img_response = requests.get(fondo_url)
    img_path = f"/tmp/{uuid.uuid4()}.jpg"
    with open(img_path, 'wb') as f:
        f.write(img_response.content)

    # Crear clip de fondo
    fondo_clip = ImageClip(img_path).set_duration(8).resize((1080, 1920))

    # Texto centrado con sombra
    txt_clip = TextClip(frase, fontsize=70, color='white', 
                        stroke_color='black', stroke_width=2,
                        method='caption', size=(900, None))
    txt_clip = txt_clip.set_position('center').set_duration(8)

    # Unir fondo y texto
    video = CompositeVideoClip([fondo_clip, txt_clip])

    # Agregar música
    audio = AudioFileClip("musica.mp3").subclip(0, 8)
    video = video.set_audio(audio)

    # Exportar
    output_path = f"/tmp/{uuid.uuid4()}.mp4"
    video.write_videofile(output_path, fps=24, codec='libx264')

    # Devolver URL del archivo
    return jsonify({"video_path": output_path, "status": "ok"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
