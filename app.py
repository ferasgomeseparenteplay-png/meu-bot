from flask import Flask, request
import random
import unicodedata
import re

app = Flask(__name__)

# 🔥 MEMÓRIA TEMPORÁRIA
nome_usuario = None

def normalizar(texto):
    texto = texto.lower().strip()
    texto = unicodedata.normalize("NFD", texto)
    texto = ''.join(c for c in texto if unicodedata.category(c) != 'Mn')
    texto = re.sub(r'(.)\1+', r'\1', texto)
    return texto

# 🔥 DETECTAR NOME
def pegar_nome(fala):
    if "meu nome é" in fala:
        return fala.replace("meu nome é", "").strip()
    if "me chamo" in fala:
        return fala.replace("me chamo", "").strip()
    if "sou o" in fala:
        return fala.replace("sou o", "").strip()
    return None

nome_bot = "Alfred"

respostas = {
    "oi": ["Fala mano", "Só de boa", "E aí parceiro", "Só o ouro derretido"],
    "olá": ["Fala mano", "Só de boa", "E aí parceiro", "Só o ouro derretido"],
    "e aí": ["Fala mano", "Só de boa", "E aí parceiro", "Só o ouro derretido"],
    "opa": ["Fala mano", "Só de boa", "E aí parceiro", "Só o ouro derretido"],
    "como vai": ["Fala mano", "Só de boa", "E aí parceiro", "Só o ouro derretido"],
    "fala aí": ["Fala mano", "Só de boa", "E aí parceiro", "Só o ouro derretido"],
    "salve": ["Fala mano", "Só de boa", "E aí parceiro", "Só o ouro derretido"],
    "beleza": ["Fala mano", "Só de boa", "E aí parceiro", "Só o ouro derretido"],
    "awire": ["Fala mano", "Só de boa", "E aí parceiro", "Só o ouro derretido"],

    "bom dia": ["Bom dia! Tudo bem?", "Bom dia, parceiro!"],
    "boa tarde": ["Boa tarde! Tudo certo?", "Boa tarde, parceiro!"],
    "boa noite": ["Boa noite! Como foi o dia?", "Boa noite, parceiro!"],
    "como você está": ["Estou bem, e você?", "Tudo ótimo, e contigo?"],

    # 🔥 PERGUNTAS DE NOME
    "qual meu nome": ["Ainda não sei seu nome 🤔", "Você ainda não me disse seu nome 😅"],
    "sabe meu nome": ["Ainda não sei 😅", "Não ainda 🤔"]
}

respostas_normalizadas = {}
for chave in respostas:
    chave_norm = normalizar(chave)
    respostas_normalizadas[chave_norm] = respostas[chave]


@app.route("/", methods=["GET", "POST"])
def home():
    global nome_usuario
    resposta = ""

    if request.method == "POST":
        fala = normalizar(request.form["msg"])

        # 🔥 DETECTAR NOME
        nome_detectado = pegar_nome(fala)
        if nome_detectado:
            nome_usuario = nome_detectado
            resposta = f"Prazer, {nome_usuario}! Vou lembrar disso 😎"

        # 🔥 SE NÃO TEM NOME AINDA
        elif not nome_usuario:
            resposta = "Qual é seu nome? 🤔"

        # 🔥 JOGO
        elif fala in ["pedra", "papel", "tesoura"]:
            computador = random.choice(["pedra", "papel", "tesoura"])

            if fala == computador:
                resposta = f"Empate! Eu escolhi {computador} 😁"
            elif (fala == "pedra" and computador == "tesoura") or \
                 (fala == "papel" and computador == "pedra") or \
                 (fala == "tesoura" and computador == "papel"):
                resposta = f"Você venceu! Eu escolhi {computador} 👏"
            else:
                resposta = f"Ganhei 😎 Eu escolhi {computador}"

        # 🔥 CHAT NORMAL
        else:
            resposta = None
            for chave in respostas_normalizadas:
                if chave in fala:
                    resposta = random.choice(respostas_normalizadas[chave])
                    break

            if not resposta:
                resposta = "Não entendi 🤔"

        # 🔥 PERSONALIZA COM NOME
        if nome_usuario and "prazer" not in resposta.lower():
            resposta = f"{nome_usuario}, {resposta}"

    return f'''
        <h1>{nome_bot}</h1>
        <form method="post">
            <input name="msg" placeholder="Digite algo">
            <button type="submit">Enviar</button>
        </form>
        <p>{resposta}</p>
    '''

app.run(host="0.0.0.0", port=10000)
