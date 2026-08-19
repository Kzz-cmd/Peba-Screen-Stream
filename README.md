# Peba Screen Stream

Um projeto simples de **transmissão de tela em tempo real** desenvolvido em Python utilizando Flask, Flask-SocketIO e PyAutoGUI.

O projeto captura a tela do computador, redimensiona e comprime cada frame em JPEG e transmite as imagens para os clientes conectados através de uma conexão Socket.IO.

O cliente não precisa instalar nenhum programa: basta acessar o endereço do servidor pelo navegador.

> **Projeto experimental/educacional.** Não foi desenvolvido com foco em segurança, eficiência ou uso em produção.

---

## Funcionalidades

- Captura da tela do computador em tempo real
- Redimensionamento para até `1280x720`
- Compressão das imagens em JPEG
- Comunicação através de Flask-SocketIO
- Visualização diretamente pelo navegador
- Suporte a múltiplos espectadores
- Limite de espectadores simultâneos
- Controle básico de requisições através do Flask-Limiter
- A captura é iniciada somente quando existe pelo menos um espectador conectado

---

## Tecnologias utilizadas

- **Python**
- **Flask** — servidor web
- **Flask-SocketIO** — comunicação em tempo real
- **PyAutoGUI** — captura da tela
- **Pillow** — processamento e redimensionamento das imagens
- **Flask-Limiter** — limitação de requisições
- **Base64** — transporte das imagens através dos eventos Socket.IO
- **HTML/CSS/JavaScript** — interface do cliente

---

## Requisitos

Python 3.x instalado.

As dependências podem ser instaladas com:

```bash
pip install flask flask-socketio flask-limiter pyautogui pillow
```

---

## Como executar

Clone o repositório:

```bash
git clone kzz-cmd
cd kzz-cmd
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Execute o servidor:

```bash
python app.py
```

O servidor será iniciado na porta `5000`.

No próprio computador, acesse:

```text
http://127.0.0.1:5000
```

Para acessar a transmissão a partir de outro dispositivo conectado à mesma rede local, descubra o IPv4 do computador que está executando o servidor e acesse:

```text
http://SEU_IP:5000
```

Por exemplo:

```text
http://192.168.1.10:5000
```

---

## ⚙️ Como funciona

O funcionamento básico do projeto é:

```text
┌──────────────────────┐
│      Computador      │
│                      │
│     PyAutoGUI        │
│          │           │
│          ▼           │
│    Captura da tela   │
│          │           │
│          ▼           │
│    Resize 1280x720   │
│          │           │
│          ▼           │
│     JPEG quality 65  │
│          │           │
│          ▼           │
│       Base64         │
│          │           │
└──────────┼───────────┘
           │
           │ Socket.IO
           ▼
┌──────────────────────┐
│      Navegador       │
│                      │
│   recebe o evento    │
│          │           │
│          ▼           │
│  data:image/jpeg...  │
│          │           │
│          ▼           │
│    <img> atualizado  │
└──────────────────────┘
```

Quando um cliente se conecta, o servidor inicia uma tarefa em background responsável por capturar e transmitir a tela.

Enquanto houver espectadores conectados, novos frames são gerados e enviados através do evento:

```text
atualiza_tela
```

O navegador recebe a imagem em Base64 e atualiza o atributo `src` de uma tag `<img>`.

---

## 👥 Limite de espectadores

O projeto possui um limite padrão de:

```python
limite_spec = 5
```

Isso significa que até cinco clientes podem assistir simultaneamente.

Quando o limite é atingido, novos clientes são desconectados.

Esse valor pode ser alterado diretamente no código.

---

## 🎥 Controle da transmissão

A transmissão possui um comportamento simples:

```text
Nenhum espectador
       ↓
   transmissão parada

Novo espectador
       ↓
 transmissão iniciada

Espectador conectado
       ↓
 captura e envio de frames

Último espectador sai
       ↓
   transmissão parada
```

Isso evita que o computador continue capturando a tela quando ninguém está assistindo.

---

## 🔧 Configurações

Algumas configurações podem ser alteradas diretamente no código.

### Resolução

Atualmente:

```python
tela.thumbnail((1280, 720))
```

### Qualidade JPEG

Atualmente:

```python
tela.save(buffer, format='JPEG', quality=65)
```

Valores maiores aumentam a qualidade da imagem, mas também aumentam o tamanho dos frames.

### Número máximo de espectadores

```python
limite_spec = 5
```

### Intervalo entre frames

Atualmente:

```python
socketio.sleep(0.01)
```

Esse valor pode ser ajustado para controlar a velocidade da transmissão.

---

## ⚠️ Limitações

Este projeto foi desenvolvido principalmente para fins de aprendizado e possui algumas limitações.

### Uso de Base64

As imagens são convertidas para Base64 antes de serem enviadas.

Isso facilita a implementação, mas adiciona overhead em relação ao envio direto dos bytes da imagem.

### Captura da tela inteira

Atualmente o projeto captura toda a tela do computador.

Não existe suporte para selecionar uma janela específica.

### Consumo de recursos

Capturar, redimensionar, comprimir e enviar imagens continuamente pode consumir uma quantidade considerável de CPU, memória e banda.

### Sem autenticação

O projeto atualmente não possui um sistema adequado de autenticação.

**Não exponha o servidor diretamente à internet sem implementar mecanismos de segurança.**

### Rede local

O projeto foi pensado inicialmente para utilização dentro de uma rede local.

Para disponibilizá-lo na internet seriam necessárias outras considerações relacionadas a firewall, NAT, exposição de portas, autenticação e segurança.

---

## 🔒 Segurança

Este projeto **não deve ser considerado seguro para exposição pública** em sua forma atual.

Qualquer pessoa que consiga acessar o servidor poderá potencialmente visualizar a transmissão.

Antes de utilizar o projeto fora de uma rede confiável, considere implementar:

- autenticação;
- autorização;
- HTTPS;
- tokens de acesso;
- controle de sessões;
- validação dos clientes;
- proteção contra abuso.

---

## 📚 Objetivo do projeto

Este projeto foi criado como um experimento para aprender conceitos relacionados a:

- servidores web;
- HTTP;
- comunicação cliente-servidor;
- WebSockets/Socket.IO;
- captura de tela;
- compressão de imagens;
- transmissão de dados em tempo real;
- programação concorrente;
- redes locais.

A ideia surgiu a partir de uma implementação anterior utilizando sockets TCP e um cliente Python com Tkinter.

A principal evolução foi substituir o cliente Python por um **navegador**, permitindo que o espectador visualize a transmissão sem precisar instalar um programa específico.

---

## 🗺️ Possíveis melhorias

Algumas ideias para versões futuras:

- [ ] Envio direto de bytes em vez de Base64
- [ ] Controle de FPS
- [ ] Interface de configuração
- [ ] Seleção de resolução
- [ ] Controle de qualidade JPEG pelo navegador
- [ ] Captura de uma janela específica
- [ ] Autenticação
- [ ] HTTPS
- [ ] Melhor gerenciamento de espectadores
- [ ] Otimização da captura e compressão
- [ ] Detecção de mudanças entre frames
- [ ] Controles remotos
- [ ] Estatísticas de FPS e consumo de banda

---

## 📄 Licença

Este projeto pode ser utilizado, estudado e modificado conforme os termos definidos pela licença deste repositório.
