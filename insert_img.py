import sqlite3
import os

# Caminho para a pasta que contém as imagens
image_folder_path = 'C:/Users/Gabriel Fernandes/Documents/face_recognition/images'

# Conecta ao banco de dados.
conn = sqlite3.connect('my_database.db')

# Crie um cursor.
c = conn.cursor()

# Lista todos os arquivos na pasta de imagens
for filename in os.listdir(image_folder_path):
    # Verifica se o arquivo é uma imagem (apenas verificando a extensão do arquivo aqui, você pode querer adicionar outras extensões ou verificar o tipo de arquivo de outra maneira)
    if filename.endswith(".jpeg") or filename.endswith(".png"):
        # Cria o caminho completo para o arquivo de imagem
        image_path = os.path.join(image_folder_path, filename)
        
        # Leia o arquivo de imagem em modo binário
        with open(image_path, 'rb') as file:
            image_data = file.read()

        # Insira a imagem no banco de dados. 
        # Aqui, eu estou usando o nome do arquivo (sem a extensão) como o nome da pessoa.
        person_name = os.path.splitext(filename)[0]
        c.execute("INSERT INTO people (name, photo) VALUES (?, ?)", (person_name, image_data))

# Salve (commit) as mudanças
conn.commit()

# Feche a conexão
conn.close()
