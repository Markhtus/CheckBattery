import sys
import time
import tkinter as tk

import psutil

LIMITE = int(sys.argv[1]) if len(sys.argv) > 1 else 80
INTERVALO = int(sys.argv[2]) if len(sys.argv) > 2 else 30


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
    continuar_ate_100 = False

    while True:
        bateria = psutil.sensors_battery()

        if bateria is None:
            break

        if not bateria.power_plugged:
            continuar_ate_100 = False

        elif bateria.percent >= LIMITE and not continuar_ate_100:
            if aviso(bateria.percent):
                continuar_ate_100 = True

        time.sleep(INTERVALO)

if __name__ == "__main__":
    main()