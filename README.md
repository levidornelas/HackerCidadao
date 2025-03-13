# Flask API para Análise de Imagens e Notificações via Telegram

Este projeto foi desenvolvido para o **Hacker Cidadão**, iniciativa da **Prefeitura do Recife**, e está enquadrado no **terceiro desafio: Governo a Zero Clique**. O objetivo é automatizar a detecção de poluição em áreas monitoradas por câmeras de segurança e enviar notificações automáticas para a prefeitura e cidadãos, sem a necessidade de intervenção manual.

## Funcionalidades
- Recebe imagens via API.
- Analisa as imagens usando a API de Visão Computacional do Azure para detectar sinais de poluição.
- Envia uma mensagem para a prefeitura se a imagem contiver sinais de poluição.
- Envia uma mensagem para os cidadãos quando a limpeza da região for concluída.
- Suporte a mensagens simuladas para testes.

## Tecnologias Utilizadas
- Python
- Flask
- Flask-CORS
- Requests
- Dotenv
- API de Visão Computacional do Azure
- API do Telegram

## Configuração e Instalação

### 1. Clone o Repositório
```sh
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
```

### 2. Crie um Ambiente Virtual (Opcional, mas Recomendado)
```sh
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate  # Windows
```

### 3. Instale as Dependências
```sh
pip install -r requirements.txt
```

### 4. Configure as Variáveis de Ambiente
Crie um arquivo `.env` e adicione suas chaves de API:
```sh
AZURE_API_KEY=your_azure_api_key
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
```

## Como Executar
```sh
python app.py
```
A API rodará em `http://127.0.0.1:5000`.

## Uso da API

### Envio de Imagem para Análise

**Endpoint:**
```http
POST /analyze-image
```

**Parâmetro:**
- `file`: Arquivo da imagem a ser analisada.

**Exemplo de Uso com cURL:**
```sh
curl -X POST -F "file=@caminho/para/imagem.jpg" http://127.0.0.1:5000/analyze-image
```

**Resposta Esperada:**
```json
{
  "tags": ["pollution", "water", "trash"],
  "description": "Imagem mostrando poluição no rio."
}
```
Se houver "pollution" nos resultados, a mensagem será enviada para a prefeitura. Caso contrário, uma mensagem de limpeza será enviada ao cidadão.

## Estrutura do Projeto
```
/
|-- app.py  # Arquivo principal do Flask
|-- .env    # Arquivo para armazenar chaves de API (não versionado)
|-- requirements.txt  # Lista de dependências
```

## Considerações
- O bot do Telegram deve estar configurado para receber e enviar mensagens corretamente.
- A API do Azure pode ter limites de uso conforme seu plano.

## Contribuição
Sinta-se à vontade para abrir issues e pull requests para melhorias.

## Licença
Este projeto está sob a licença MIT.

