import os
import sys
import time
import tkinter as tk
from datetime import datetime

import psutil

LIMITE = int(sys.argv[1]) if len(sys.argv) > 1 else 80
INTERVALO = int(sys.argv[2]) if len(sys.argv) > 2 else 30  
INTERVALO_BATERIA = int(sys.argv[3]) if len(sys.argv) > 3 else 60 

PASTA_LOG = os.path.join(
    os.environ.get("LOCALAPPDATA", os.path.expanduser("~")), "CheckBattery"
)
ARQUIVO_LOG = os.path.join(PASTA_LOG, "log.txt")


def log(msg):
    try:
        os.makedirs(PASTA_LOG, exist_ok=True)
        if os.path.exists(ARQUIVO_LOG) and os.path.getsize(ARQUIVO_LOG) > 200_000:
            os.remove(ARQUIVO_LOG)
        with open(ARQUIVO_LOG, "a", encoding="utf-8") as f:
            f.write(f"{datetime.now():%Y-%m-%d %H:%M:%S}  {msg}\n")
    except Exception:
        pass


def aviso(percent):
    escolha = {"continuar": False}

    root = tk.Tk()
    root.title("Preservar bateria")
    root.attributes("-topmost", True)
    root.resizable(False, False)

    root.protocol("WM_DELETE_WINDOW", lambda: None)

    texto = tk.Label(
        root,
        text="",
        font=("Segoe UI", 11),
        justify="center",
        padx=25,
        pady=20,
    )
    texto.pack()

    def atualizar_texto(p):
        texto.config(
            text=f"A bateria está em {p}%.\n\n"
                 "Para preservar a vida útil da bateria,\n"
                 "remova o carregador da tomada.\n\n"
                 "Este aviso fechará assim que você desconectar."
        )

    def continuar():
        escolha["continuar"] = True
        root.destroy()

    botao = tk.Button(
        root,
        text="Continuar carregando até 100%",
        font=("Segoe UI", 10),
        command=continuar,
        padx=10,
        pady=5,
    )
    botao.pack(pady=(0, 20))

    def checar():
        bateria = psutil.sensors_battery()
        if bateria is None or not bateria.power_plugged:
            root.destroy()
            return
        atualizar_texto(bateria.percent)
        root.after(1000, checar)

    atualizar_texto(percent)
    root.after(1000, checar)

    root.update_idletasks()
    largura = root.winfo_width()
    altura = root.winfo_height()
    x = (root.winfo_screenwidth() - largura) // 2
    y = (root.winfo_screenheight() - altura) // 2
    root.geometry(f"+{x}+{y}")

    root.mainloop()
    return escolha["continuar"]


def main():
    log(f"Programa iniciado (limite={LIMITE}%)")
    continuar_ate_100 = False
    falhas_leitura = 0

    while True:
        espera = INTERVALO
        try:
            bateria = psutil.sensors_battery()

            if bateria is None:
                falhas_leitura += 1
                log(f"Leitura da bateria indisponível ({falhas_leitura}/10)")
                if falhas_leitura >= 10:
                    log("Nenhuma bateria detectada. Encerrando.")
                    break
                time.sleep(INTERVALO)
                continue

            falhas_leitura = 0

            if not bateria.power_plugged:
                if continuar_ate_100:
                    log("Carregador removido: ciclo reiniciado")
                continuar_ate_100 = False
                espera = INTERVALO_BATERIA

            elif bateria.percent >= LIMITE and not continuar_ate_100:
                log(f"Aviso exibido em {bateria.percent}%")
                if aviso(bateria.percent):
                    continuar_ate_100 = True
                    log("Usuário escolheu continuar até 100%")
                else:
                    log("Carregador removido: aviso fechado")

        except Exception as erro:
            log(f"ERRO: {erro!r}")

        time.sleep(espera)


if __name__ == "__main__":
    main()