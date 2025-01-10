# PhoneLink: Transferência de Arquivos e Dados Entre Dispositivos

## Descrição

O **PhoneLink** é uma aplicação desenvolvida em Python que permite a transferência de imagens, arquivos e textos entre dispositivos por meio de um servidor web. Ela oferece a funcionalidade de enviar dados de um dispositivo para outro, copiar para a área de transferência, salvar arquivos, salvar imagens e até desligar o dispositivo remotamente através de uma interface de servidor baseada no **Flask**.

Além disso, a aplicação conta com um ícone de bandeja, que oferece acesso rápido ao log de atividades e à última imagem salva.

## Funcionalidades

### 1. **Desligamento Remoto do Sistema**
   - A aplicação possui um endpoint `/desligar` que, ao receber uma requisição com um código de senha (`coolpassword`), executa um comando para desligar o computador imediatamente.
   - **Método:** `POST`
   - **Dados:** JSON com a chave `data` contendo o valor `coolpassword`.

### 2. **Transferência de Texto para a Área de Transferência**
   - A aplicação recebe um texto via requisição `POST` no endpoint `/copy` e o copia para a área de transferência do dispositivo.
   - **Método:** `POST`
   - **Dados:** JSON com a chave `text` contendo o texto a ser copiado.

### 3. **Salvar Arquivos**
   - Arquivos enviados ao endpoint `/save_file` são salvos em um diretório no sistema e o caminho do arquivo é copiado para a área de transferência.
   - **Método:** `POST`
   - **Dados:** Arquivo a ser enviado.
   - O sistema automaticamente remove arquivos antigos e garante que apenas um arquivo por vez seja salvo.

### 4. **Salvar e Copiar Imagens**
   - A aplicação recebe uma imagem via requisição `POST` no endpoint `/save_image`, salva-a em um diretório especificado e a copia para a área de transferência.
   - **Método:** `POST`
   - **Dados:** Imagem a ser enviada.
   - As imagens são rotacionadas automaticamente, caso estejam na orientação incorreta.

### 5. **Interface de Bandeja (System Tray)**
   - Um ícone de bandeja permite:
     - Abrir o arquivo de log de atividades.
     - Abrir a última foto salva no sistema.
     - Fechar a aplicação.

### 6. **Log de Atividades**
   - A aplicação mantém um log completo de todas as operações realizadas no arquivo `flask_server.log`. O log pode ser acessado diretamente através do ícone de bandeja.

## Pré-requisitos

Antes de rodar a aplicação, certifique-se de ter o seguinte instalado em seu sistema:

- Python 3.6 ou superior
- Flask
- Pystray
- Pillow (PIL)
- Paho MQTT
- pyperclip
- win32clipboard
- win32con

### Instalar dependências

Execute o seguinte comando para instalar as dependências necessárias:

```bash
pip install flask pystray Pillow paho-mqtt pyperclip pywin32
