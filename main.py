import face_recognition
import cv2
import numpy as np
import os
import glob
import sqlite3
import tkinter as tk
from tkinter import messagebox
import time

# Crie a janela tkinter e imediatamente a esconda
root = tk.Tk()
root.withdraw()

# Carregar rostos conhecidos
known_faces = []
known_names = []

# Conectar ao banco de dados SQLite
conn = sqlite3.connect('my_database.db')
c = conn.cursor()

# Recuperar todas as entradas da tabela de pessoas
c.execute('SELECT * FROM people')

rows = c.fetchall()

for row in rows:
    name = row[0]
    image_data = row[1]
    
    # Criar uma imagem a partir dos dados
    nparr = np.frombuffer(image_data, np.uint8)  # Use np.frombuffer em vez de np.fromstring
    img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Carregar a imagem para face_recognition e aprender a codificar
    face_encoding = face_recognition.face_encodings(img_np)[0]
    known_faces.append(face_encoding)
    known_names.append(name)

# Iniciar o vídeo
video_capture = cv2.VideoCapture(0)

# Inicializar a variável de tempo
last_time_alerted = time.time()

while True:
    # Pegue um único frame de vídeo
    ret, frame = video_capture.read()

    # Reduzir o tamanho do frame para 1/4 para processamento mais rápido
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Converter a imagem de BGR (que o OpenCV usa) para a cor RGB (que face_recognition usa)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Encontrar todas as faces e codificações de rosto no frame atual do vídeo
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    face_names = []
    for face_encoding in face_encodings:
        # Veja se a face é uma correspondência dos rostos conhecidos
        matches = face_recognition.compare_faces(known_faces, face_encoding)
        name = "Unknown"

        # Se uma correspondência foi encontrada na known_face_encodings, apenas use o primeiro.
        if True in matches:
            first_match_index = matches.index(True)
            name = known_names[first_match_index]
            
            # Verifique se já se passaram 5 segundos desde o último alerta
            if time.time() - last_time_alerted > 5:
                messagebox.showinfo("Face Recognition Alert", f"{name} was recognized!")
                last_time_alerted = time.time()

        face_names.append(name)

    # Exiba os resultados
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Escalar o local do rosto de volta ao tamanho original
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Desenhe um retângulo em torno do rosto
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Desenhe uma caixa de etiqueta com um nome abaixo do rosto
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Exiba o frame final resultante
    cv2.imshow('Video', frame)

    # Sair do loop no pressionar da tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar handle para a webcam
video_capture.release()
cv2.destroyAllWindows()