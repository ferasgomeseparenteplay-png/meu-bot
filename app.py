from flask import Flask, request
import random
import unicodedata
import re

app = Flask(__name__)

def normalizar(texto):
    texto = texto.lower().strip()
    texto = unicodedata.normalize("NFD", texto)
    texto = ''.join(c for c in texto if unicodedata.category(c) != 'Mn')
    texto = re.sub(r'(.)\1+', r'\1', texto)
    return texto

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
    "como você está": ["Estou bem, e você?", "Tudo ótimo, e contigo?"]
}

respostas_normalizadas = {}
for chave in respostas:
    chave_norm = normalizar(chave)
    respostas_normalizadas[chave_norm] = respostas[chave]


@app.route("/", methods=["GET", "POST"])
def home():
    resposta = ""

    if request.method == "POST":
        fala = normalizar(request.form["msg"])

        # 🔥 JOGO
        if fala in ["pedra", "papel", "tesoura"]:
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

    return f'''
        <h1>{nome_bot}</h1>
        <form method="post">
            <input name="msg" placeholder="Digite algo">
            <button type="submit">Enviar</button>
        </form>
        <p>{resposta}</p>
    '''

app.run()