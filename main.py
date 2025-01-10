from flask import Flask, request
import pystray
from PIL import Image, ImageDraw, ExifTags
import logging
import sys
import os
import threading
import paho.mqtt.client as mqtt
import io
import pyperclip
import win32clipboard as clipboard
import win32con
import subprocess

app = Flask(__name__)

#OBS: CRIAR PHONELINK DIR (CHECAR SE EXISTE)

# Configuração do logging para redirecionar os logs para um arquivo
logging.basicConfig(filename='C:/phoneLink/flask_server.log', level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

@app.route('/desligar', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        data = request.get_json()  # Se a requisição for POST, espera receber dados em JSON
        logging.info(f'Recebido: {data}')
        if data['data'] == 'coolpassword':
          os.system('shutdown /s /t 1')
          return f'Recebido: {data}', 200
    else:
        return 'Aplicação rodando na porta 8211', 200

    
    
@app.route('/copy', methods=['POST'])
def copy_to_clipboard():
    data = request.get_json()
    if 'text' in data:
        text = data['text']
        pyperclip.copy(text)
        logging.info(f"Texto copiado para a área de transferência: {text}")
        
        # Open the file in append mode ('a') to add a line at the end of the file
        import datetime

        # Obter a data e hora atual
        now = datetime.datetime.now()
        formatted_time = now.strftime("%H:%M %d/%m/%Y")

        # Texto a ser adicionado
        text_to_add = text

        # Abrir o arquivo em modo de append ('a') para adicionar a linha no final
        with open('historico.txt', 'a') as file:
            # Escrever a data/hora e o texto no arquivo
            file.write(f"{text_to_add} -{formatted_time}\n")

        return 'Texto copiado para a área de transferência.', 200
    return 'Nenhum texto fornecido.', 400

@app.route('/save_file', methods=['POST'])
def save_file():
    if 'file' in request.files:
        file = request.files['file']
        filename = f"upload.{file.filename.split('.')[-1]}"
        upload_path = 'C:/phoneLink/uploads'

        # Cria a pasta se não existir
        os.makedirs(upload_path, exist_ok=True)

        # Remove arquivos existentes na pasta
        for existing_file in os.listdir(upload_path):
            file_path = os.path.join(upload_path, existing_file)
            if os.path.isfile(file_path):
                os.remove(file_path)

        # Define o caminho completo para salvar o novo arquivo
        file_path = os.path.join(upload_path, filename)

        try:
            # Salva o novo arquivo
            file.save(file_path)
            logging.info(f"Arquivo salvo em: {file_path}")

            # Coloca o caminho do arquivo na área de transferência
            colocar_arquivo_no_clipboard(file_path)

            return f'Arquivo salvo e caminho copiado para a área de transferência: {file_path}', 200
        except Exception as e:
            logging.error(f"Erro ao salvar ou copiar o arquivo: {e}")
            return 'Erro ao salvar ou copiar o arquivo.', 500

    return 'Nenhum arquivo fornecido.', 400

def colocar_arquivo_no_clipboard(caminho_arquivo):
    file_path = caminho_arquivo  # caminho do arquivo

    # Comando PowerShell para copiar o arquivo para a área de transferência
    command = f'powershell -command "Set-Clipboard -Path \'{file_path}\'"'

    # Executa o comando
    try:
        subprocess.run(command, shell=True, check=True)
        print(f"Arquivo '{file_path}' copiado para a área de transferência.")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao copiar o arquivo: {e}")

    #os.startfile(caminho_arquivo) abrir o arquivo
    logging.info("Caminho do arquivo copiado para a área de transferência!")


# Função para copiar a imagem para a área de transferência
def copiar_imagem_para_clipboard(caminho_imagem):
    # Abre a imagem e converte para o formato BMP, que o Windows usa na área de transferência
    imagem = Image.open(caminho_imagem)
    output = io.BytesIO()
    imagem.convert("RGB").save(output, "BMP")
    dados_bmp = output.getvalue()[14:]  # Remove o cabeçalho de 14 bytes do BMP

    # Copia a imagem para a área de transferência
    clipboard.OpenClipboard()
    clipboard.EmptyClipboard()
    clipboard.SetClipboardData(clipboard.CF_DIB, dados_bmp)
    clipboard.CloseClipboard()

    logging.info("Imagem copiada para a área de transferência!")



@app.route('/save_image', methods=['POST'])
def save_image():
    if 'image' in request.files:
        image_file = request.files['image']
        logging.info("Imagem recebida.")
        
        try:
            # Abre a imagem, independentemente do formato
            image = Image.open(image_file.stream)

            # Verifica a orientação da imagem e a rotaciona se necessário
            if image.width > image.height:
                image = image.rotate(-90, expand=True)  # Rotaciona 90 graus no sentido horário

            image_path = 'C:/phoneLink/saved_image.png'  # Define o caminho para salvar a imagem
            image.save(image_path)  # Salva a imagem no caminho especificado
    
            # Copia a imagem para a área de transferência
            colocar_arquivo_no_clipboard(image_path)

            logging.info(f"Imagem salva em: {image_path} e copiada para a área de transferência.")
            return f'Imagem salva em: {image_path}', 200
        except Exception as e:
            logging.error(f"Erro ao salvar imagem: {e}")
            return 'Erro ao salvar imagem.', 500

    return 'Nenhuma imagem fornecida.', 400

def run_flask():
    app.run(host='0.0.0.0', port=8211)

def create_image():
    # Cria uma imagem para o ícone da bandeja
    width = 64
    height = 64
    image = Image.new('RGB', (width, height), (255, 255, 255))
    dc = ImageDraw.Draw(image)
    dc.rectangle(
        (width // 2 - width // 4, height // 2 - height // 4, width // 2 + width // 4, height // 2 + height // 4),
        fill='black')
    return image

def on_quit(icon, item):
    # Função para sair da aplicação
    icon.stop()
    sys.exit()

def open_log_file(icon, item):
    # Função para abrir o arquivo de log
    if os.name == 'nt':  # Windows
        os.startfile('C:/phoneLink/flask_server.log')
def open_last_photo():
    caminho_imagem = "C:/phoneLink/saved_image.png"
    # Abre a imagem com o visualizador de imagens padrão do sistema
    os.startfile(caminho_imagem) 
def setup_tray_icon():
    # Configuração do ícone da bandeja
    icon_image = create_image()
    icon = pystray.Icon("Flask Server", icon_image, "Flask Server", menu=pystray.Menu(
        pystray.MenuItem("Open Log File", open_log_file),
        pystray.MenuItem("Abrir ultima foto", open_last_photo),
        pystray.MenuItem("Quit", on_quit)
    ))
    icon.run()


if __name__ == '__main__':
    # Inicia o servidor Flask em um thread separado
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()

    # Configura e inicia o ícone da bandeja
    setup_tray_icon()
