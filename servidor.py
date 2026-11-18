from flask import Flask, request, jsonify
import random
import json
import os

app = Flask(__name__)

ARQUIVO = "dados.json"
JOGADAS = ["pedra", "papel", "tesoura"]
VENCE = {"pedra": "tesoura", "tesoura": "papel", "papel": "pedra"}
CONTRA = {perdedor: vencedor for vencedor, perdedor in VENCE.items()}


def carregar():
    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, "r", encoding="utf-8") as f:
            return json.load(f)
    return novo_placar()


def novo_placar():
    return {
        "historico": {"pedra": 0, "papel": 0, "tesoura": 0},
        "vitorias": 0,
        "derrotas": 0,
        "empates": 0,
    }


def salvar(dados):
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)


def escolher_jogada_do_computador(historico):
    total = sum(historico.values())
    if total >= 3 and random.random() < 0.7:
        favorita = max(historico, key=historico.get)
        return CONTRA[favorita], True
    return random.choice(JOGADAS), False


@app.route("/jogar", methods=["POST"])
def jogar():
    dados = carregar()
    jogador = request.json.get("jogada")

    if jogador not in JOGADAS:
        return jsonify({"erro": "Jogada inválida"}), 400

    computador, previu = escolher_jogada_do_computador(dados["historico"])

    if jogador == computador:
        resultado = "empate"
        dados["empates"] += 1
    elif VENCE[jogador] == computador:
        resultado = "vitoria"
        dados["vitorias"] += 1
    else:
        resultado = "derrota"
        dados["derrotas"] += 1

    dados["historico"][jogador] += 1
    salvar(dados)

    return jsonify({
        "computador": computador,
        "resultado": resultado,
        "previu": previu,
        "placar": dados,
    })


@app.route("/placar", methods=["GET"])
def placar():
    return jsonify(carregar())


@app.route("/resetar", methods=["POST"])
def resetar():
    dados = novo_placar()
    salvar(dados)
    return jsonify(dados)


if __name__ == "__main__":
    app.run(port=5000)