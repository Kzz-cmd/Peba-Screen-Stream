[README — Peba Screen Stream.md](https://github.com/user-attachments/files/31227889/README.Peba.Screen.Stream.md)
# Peba Screen Stream

Um projeto simples de **transmissão de tela em tempo real para redes locais**, desenvolvido em Python utilizando Flask, Flask-SocketIO e PyAutoGUI.

O projeto captura a tela do computador, redimensiona e comprime cada frame em JPEG e transmite as imagens para os clientes conectados através de uma conexão Socket.IO.

O cliente não precisa instalar nenhum programa: basta acessar o endereço do servidor pelo navegador através da rede local.

> **Projeto experimental/educacional.** O foco do projeto é aprendizado e utilização em redes locais, não sendo destinado a substituir soluções profissionais de transmissão ou acesso remoto.

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

Para acessar a transmissão a partir de outro dispositivo conectado à **mesma rede local**, descubra o IPv4 do computador que está executando o servidor e acesse:

```text
http://SEU_IP:5000
```

Por exemplo:

```text
http://192.168.1.10:5000
```

> O projeto foi pensado justamente para esse cenário: um computador hospeda a transmissão e outros dispositivos da mesma rede podem visualizá-la através do navegador.

---

## Como funciona

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

Quando o último espectador se desconecta, a captura é interrompida.

---

## Gerenciamento de espectadores

O projeto possui um limite padrão de:

```python
limite_spec = 5
```

Isso significa que até cinco clientes podem assistir simultaneamente.

Quando o limite é atingido, novos clientes são desconectados.

Esse sistema também permite que a transmissão seja iniciada e interrompida automaticamente de acordo com a quantidade de espectadores:

```text
Nenhum espectador
       ↓
   transmissão parada

Novo espectador
       ↓
 transmissão iniciada

Espectadores conectados
       ↓
 captura e envio de frames

Último espectador sai
       ↓
   transmissão parada
```

Esse comportamento evita capturas desnecessárias quando ninguém está assistindo.

---

## Configurações

Algumas configurações podem ser alteradas diretamente no código.

### Resolução

Atualmente:

```python
tela.thumbnail((1280, 720))
```

A resolução pode ser ajustada de acordo com a necessidade da rede e dos dispositivos que irão visualizar a transmissão.

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

Esse valor influencia a frequência com que novos frames são capturados e enviados.

---

## Considerações

O projeto foi desenvolvido com **redes locais em mente**.

Ele não tem como objetivo ser uma ferramenta de acesso remoto pela internet ou substituir soluções como ferramentas profissionais de streaming e acesso remoto.

### Uso de Base64

As imagens são convertidas para Base64 antes de serem enviadas.

Isso simplifica o transporte das imagens através dos eventos Socket.IO, mas adiciona overhead em relação ao envio direto dos bytes.

### Captura da tela inteira

Atualmente o projeto captura toda a tela do computador.

Não existe suporte para selecionar uma janela específica.

### Consumo de recursos

Capturar, redimensionar, comprimir e transmitir imagens continuamente utiliza CPU, memória e largura de banda.

Por isso, resolução, qualidade e frequência dos frames possuem impacto direto no desempenho.

### Segurança

Embora o projeto tenha como objetivo o uso em redes locais, ele **não possui autenticação**.

Por isso, deve ser utilizado apenas em redes nas quais os dispositivos conectados sejam confiáveis.

Não é recomendado expor a porta do servidor diretamente à internet.

---

## Objetivo do projeto

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

Na implementação anterior, era necessário executar um programa cliente para receber as imagens.

A principal evolução deste projeto foi substituir esse cliente por um **navegador**, permitindo que qualquer dispositivo conectado à mesma rede local possa visualizar a transmissão sem precisar instalar um programa específico.

---

## Possíveis melhorias

Algumas melhorias planejadas ou consideradas para versões futuras:

- [ ] Controle de FPS
- [ ] Seleção de resolução
- [ ] Controle de qualidade JPEG
- [ ] Melhor gerenciamento de espectadores
- [ ] Interface para configurar a transmissão
- [ ] Exibição de FPS atual
- [ ] Exibição do consumo aproximado de banda
- [ ] Otimização da captura e compressão
- [ ] Envio direto dos bytes da imagem em vez de Base64
- [ ] Melhor gerenciamento da tarefa de transmissão
- [ ] Seleção de uma janela específica para captura

---

## Licença

Este projeto pode ser utilizado, estudado e modificado conforme os termos definidos pela licença deste repositório.
