from flask import Flask, request, jsonify
import requests
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

app = Flask(__name__)
CORS(app)

# Função para analisar a imagem com a API do Azure
def analyze_image(image_path):
    AZURE_API_KEY = os.getenv('AZURE_API_KEY')
    AZURE_ENDPOINT = 'https://hackercidadao.cognitiveservices.azure.com/vision/v3.2/analyze'
    visual_features = 'Categories,Description,Tags'

    with open(image_path, 'rb') as image_file:
        image_data = image_file.read()

    headers = {
        'Ocp-Apim-Subscription-Key': AZURE_API_KEY,
        'Content-Type': 'application/octet-stream'
    }

    params = {
        'visualFeatures': visual_features
    }

    response = requests.post(
        AZURE_ENDPOINT,
        headers=headers,
        params=params,
        data=image_data  # Envia o arquivo binário diretamente
    )

    if response.status_code == 200:
        return response.json()
    else:
        return None

# Função para enviar mensagem para a prefeitura
def send_message_to_prefecture(image_path):
    message = """
    Alerta de Poluição: 
    Uma imagem capturada por câmeras de segurança foi analisada e contém indicadores de poluição na área.

    Localização: Rio Capibaribe (Ponto X, exemplo de coordenada aproximada)

    Detalhes da Análise:
    - A imagem foi classificada com a tag: Poluição.
    - A área identificada pode estar sofrendo com condições inadequadas de saneamento e poluição, o que requer fiscalização imediata.

    Ação Recomendada:
    Recomendamos que a equipe de fiscalização da prefeitura realize uma vistoria na área indicada. A situação precisa ser avaliada para garantir um ambiente saudável.

    Imagem Enviada pela Câmera de Segurança:
    Abaixo está a imagem capturada pelas câmeras de segurança, que deve ser verificada.
    """
    # Envia a imagem junto com a mensagem
    send_telegram_message_with_image(message, image_path)

# Função para enviar a imagem com a mensagem no Telegram
def send_telegram_message_with_image(message, image_path):
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    CHAT_ID = '7612108759'

    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto'
    payload = {
        'chat_id': CHAT_ID,
        'caption': message
    }
    files = {
        'photo': open(image_path, 'rb')
    }

    response = requests.post(url, data=payload, files=files)

    return response.status_code == 200

# Função para enviar mensagem para o cidadão após a limpeza
def send_message_to_citizen(image_path):
    message = """
    Olá! Prefeitura do Recife passando!🌟

    A área em que você reside foi limpa! 🧹🌱 Através das câmeras de segurança, detectamos a necessidade de ação e, agora, a situação foi resolvida.

    Seu direito ao saneamento básico e à limpeza é fundamental, e a Prefeitura está atenta para garantir que a qualidade de vida na sua região seja sempre a melhor possível.

    Agradecemos por sua paciência e colaboração. Estamos monitorando constantemente para garantir que sua área continue limpa e segura.

    Imagem Capturada por Câmeras de Segurança:
    Veja a imagem analisada que indicou a necessidade de ação. A situação foi resolvida e sua área agora está livre da poluição!

    O saneamento básico é um direito de todos. Estamos aqui para garantir que isso seja respeitado!
    """
    # Envia a imagem junto com a mensagem
    send_telegram_message_with_image(message, image_path)

# Função para determinar para quem a mensagem será enviada, dependendo do público
def send_pollution_notification_to_telegram(image_path, result):
    # Verifica se há a tag "Pollution" nos resultados da análise da imagem
    if "pollution" in result.get("tags", []):
        # Se houver tag de poluição, envia para a prefeitura
        send_message_to_prefecture(image_path)
    else:
        # Caso contrário, NÃO há poluição, então envia para o cidadão
        send_message_to_citizen(image_path)

# Função para enviar uma mensagem simulada para a prefeitura
def send_simulated_message_to_prefecture(image_path):
    simulated_message = """
    [MENSAGEM SIMULADA] Alerta de Poluição: 
    Uma imagem capturada por câmeras de segurança foi analisada e contém indicadores de poluição na área.

    Localização: Rio Capibaribe (Ponto X, exemplo de coordenada aproximada)

    Detalhes da Análise:
    - A imagem foi classificada com a tag: Poluição.
    - A área identificada pode estar sofrendo com condições inadequadas de saneamento e poluição, o que requer fiscalização imediata.

    Ação Recomendada:
    Recomendamos que a equipe de fiscalização da prefeitura realize uma vistoria na área indicada. A situação precisa ser avaliada para garantir um ambiente saudável.

    Imagem Enviada pela Câmera de Segurança:
    Abaixo está a imagem capturada pelas câmeras de segurança, que deve ser verificada.
    """
    # Envia a imagem junto com a mensagem simulada
    send_telegram_message_with_image(simulated_message, image_path)

# Rota para analisar a imagem e enviar a notificação
@app.route('/analyze-image', methods=['POST'])
def analyze_image_route():
    image_file = request.files['file']
    image_path = './uploaded_image.jpg'
    image_file.save(image_path)
    
    result = analyze_image(image_path)
    if result:
        print("Resultado da análise da imagem:")
        print(result)
        
        # Envia a notificação com base nos resultados da análise
        send_pollution_notification_to_telegram(image_path, result)
        
        return jsonify(result), 200
    else:
        print("Erro ao analisar a imagem.")
        return jsonify({"error": "An error occurred during analysis."}), 400

if __name__ == '__main__':
    app.run(debug=True)