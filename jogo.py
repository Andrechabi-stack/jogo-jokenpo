import tkinter as tk
from tkinter import messagebox
import requests

URL = "http://127.0.0.1:5000"
EMOJIS = {"pedra": "✊", "papel": "✋", "tesoura": "✌️"}


def jogar(jogada):
    try:
        resp = requests.post(f"{URL}/jogar", json={"jogada": jogada}, timeout=3)
        dados = resp.json()
    except requests.exceptions.RequestException:
        messagebox.showerror("Erro", "Servidor desligado! Rode: python servidor.py")
        return

    lbl_duelo.config(
        text=f"Você: {EMOJIS[jogada]}   x   PC: {EMOJIS[dados['computador']]}"
    )

    textos = {
        "vitoria": ("🎉 Você venceu!", "green"),
        "derrota": ("😈 O computador venceu!", "red"),
        "empate": ("🤝 Empate!", "gray"),
    }
    texto, cor = textos[dados["resultado"]]
    lbl_resultado.config(text=texto, fg=cor)

    if dados["previu"]:
        lbl_dica.config(text="🧠 O PC previu seu padrão!")
    else:
        lbl_dica.config(text="🎲 O PC jogou no chute.")

    atualizar_placar(dados["placar"])


def atualizar_placar(p):
    lbl_placar.config(
        text=f"Vitórias: {p['vitorias']}   Derrotas: {p['derrotas']}   Empates: {p['empates']}"
    )
    h = p["historico"]
    lbl_historico.config(
        text=f"Suas jogadas → ✊ {h['pedra']}  ✋ {h['papel']}  ✌️ {h['tesoura']}"
    )


def resetar():
    if messagebox.askyesno("Resetar", "Apagar todo o histórico?"):
        try:
            dados = requests.post(f"{URL}/resetar", timeout=3).json()
            atualizar_placar(dados)
            lbl_duelo.config(text="")
            lbl_resultado.config(text="Faça sua jogada!", fg="black")
            lbl_dica.config(text="")
        except requests.exceptions.RequestException:
            messagebox.showerror("Erro", "Servidor desligado!")


janela = tk.Tk()
janela.title("Pedra, Papel e Tesoura: O Adversário que Aprende")
janela.geometry("460x420")

tk.Label(janela, text="Pedra, Papel e Tesoura", font=("Arial", 18, "bold")).pack(pady=10)
lbl_resultado = tk.Label(janela, text="Faça sua jogada!", font=("Arial", 14))
lbl_resultado.pack()
lbl_duelo = tk.Label(janela, text="", font=("Arial", 20))
lbl_duelo.pack(pady=10)
lbl_dica = tk.Label(janela, text="", font=("Arial", 10, "italic"))
lbl_dica.pack()

frame = tk.Frame(janela)
frame.pack(pady=15)
for nome in ["pedra", "papel", "tesoura"]:
    tk.Button(
        frame,
        text=f"{EMOJIS[nome]}\n{nome.capitalize()}",
        font=("Arial", 14),
        width=8,
        command=lambda n=nome: jogar(n),
    ).pack(side="left", padx=8)

lbl_placar = tk.Label(janela, text="", font=("Arial", 11, "bold"))
lbl_placar.pack(pady=5)
lbl_historico = tk.Label(janela, text="", font=("Arial", 10))
lbl_historico.pack()
tk.Button(janela, text="Resetar histórico", command=resetar).pack(pady=10)

try:
    atualizar_placar(requests.get(f"{URL}/placar", timeout=3).json())
except requests.exceptions.RequestException:
    messagebox.showwarning("Aviso", "Servidor desligado! Rode: python servidor.py")

janela.mainloop()