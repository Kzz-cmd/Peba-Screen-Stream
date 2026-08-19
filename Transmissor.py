#Importação de bibliotecas
from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from io import BytesIO
from PIL import Image
from flask_socketio import SocketIO,disconnect
from mss import mss

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
    with mss() as sct:
        while transmissao and espectadores > 0:
            #Serão tiradas prints no monitor principal
            sct_img = sct.grab(sct.monitors[1])

            #Converte a captura do MSS para uma imagem do Pillow (PIL)
            tela = Image.frombytes("RGB",sct_img.size,sct_img.bgra,"raw","BGRX")

            #Essas prints serão redimensionadas para resolução de 1280x720
            tela.thumbnail((1280,720))
            buffer = BytesIO()
            #As prints serão salvas na memória ram do computador com uma qualidade baixa
            tela.save(buffer,format='JPEG',quality=65)

            #Ao transformar as prints em bytes, ela é enviada
            socketio.emit('atualiza_tela',{'imagem':buffer.getvalue()})

            socketio.sleep(1/60) #Definir a quantia de quadros por segundo
        transmissao = False

@socketio.on('connect')
def quando_cliente_conectar():
    global transmissao, espectadores
    #O código vai desconectar quem aparecer a mais do limite
    if espectadores >= limite_spec:
        disconnect()
        return False
    
    #Caso não, ele vai adicionar mais um no contador de espectadores
    espectadores += 1

    #Alguém ao entrar na transmissão, ligará ela
    if not transmissao:
        transmissao = True
        socketio.start_background_task(gerar_e_enviar_telas)

@socketio.on('disconnect')
def quando_cliente_desconectar():
    global espectadores
    #Quando alguém sair diminuirá o contador
    if espectadores > 0:
        espectadores -= 1

@app.route("/")
def home():
    return '''
    <html>
        <head>
            <title>Transmissão Peba</title>
            <link rel="icon" href="data:,">
            <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js"></script>
        </head>
        <body style="background-color: #222; color: white; text-align: center;">
            <img id="minha-tela" style="max-width: 80%; border: 2px solid #4CAF50;" alt="Aguardando conexão...">
            <script>
                var socket = io();
                var imagemElement = document.getElementById("minha-tela")
                var urlAnterior = null;

                socket.on("atualiza_tela", function(dados) {
                    var blob = new Blob([dados.imagem],{type:"image/jpeg"});
                    var urlAtual = URL.createObjectURL(blob);
                    imagemElement.src = urlAtual;
                    imagemElement.onload = function(){
                        if (urlAnterior){
                        URL.revokeObjectURL(urlAnterior);
                        }
                        urlAnterior = urlAtual;
                    };
                });
                
                socket.on("disconnect", function() {
                    document.getElementById("minha-tela").alt = "Transmissão lotada ou encerrada.";
                });
            </script>
        </body>
    </html>'''
socketio.run(host='0.0.0.0',app=app)