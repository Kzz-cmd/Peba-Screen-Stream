#Importação de bibliotecas
from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from pyautogui import screenshot
import base64
from io import BytesIO
from flask_socketio import SocketIO,disconnect

#Servidor
app = Flask(__name__)
socketio = SocketIO(app)

#Limitador
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["100 per day","10 per minute"]
)

transmissao = False
espectadores = 0
limite_spec = 5

def gerar_e_enviar_telas():
    global transmissao,espectadores
    #Enquanto ter pessoas vendo a transmissão
    while transmissao and espectadores > 0:
        #Serão tiradas prints
        tela = screenshot()
        #Essas prints serão redimensionadas para resolução de 1280x720
        tela.thumbnail((1280,720))
        buffer = BytesIO()
        #As prints serão salvas na memória ram do computador com uma qualidade baixa
        tela.save(buffer,format='JPEG',quality=65)
        imagem_texto = base64.b64encode(buffer.getvalue()).decode('utf-8')
        socketio.emit('atualiza_tela',{'imagem':imagem_texto})
        socketio.sleep(0.01) #mecher nisso pra deixar mais rápido
    transmissao = False

@socketio.on('connect')
def quando_cliente_conectar():
    global transmissao, espectadores
    
    if espectadores >= limite_spec:
        disconnect()
        return False
        
    espectadores += 1
    
    if not transmissao:
        transmissao = True
        socketio.start_background_task(gerar_e_enviar_telas)

@socketio.on('disconnect')
def quando_cliente_desconectar():
    global espectadores
    if espectadores > 0:
        espectadores -= 1

@app.route("/")
def home():
    return '''
    <html>
        <head>
            <title>Transmissão Peba</title>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js"></script>
        </head>
        <body style="background-color: #222; color: white; text-align: center;">
            <img id="minha-tela" style="max-width: 80%; border: 2px solid #4CAF50;" alt="Aguardando conexão...">
            <script>
                var socket = io();
                
                socket.on("atualiza_tela", function(dados) {
                    var imagem = document.getElementById("minha-tela");
                    imagem.src = "data:image/jpeg;base64," + dados.imagem;
                });
                
                socket.on("disconnect", function() {
                    document.getElementById("minha-tela").alt = "Transmissão lotada ou encerrada.";
                });
            </script>
        </body>
    </html>'''
socketio.run(host='0.0.0.0',app=app)