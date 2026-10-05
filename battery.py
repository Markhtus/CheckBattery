import sys
import time
import tkinter as tk

import psutil

# Uso normal: python bateria.py
# Uso em teste: python bateria.py 60 5
LIMITE = int(sys.argv[1]) if len(sys.argv) > 1 else 80
INTERVALO = int(sys.argv[2]) if len(sys.argv) > 2 else 30


def aviso(percent):
    """
    Mostra a janela e só retorna quando:
      - o usuário clicar em "Continuar carregando" -> retorna True
      - o carregador for removido                  -> retorna False
    """
    escolha = {"continuar": False}

    root = tk.Tk()
    root.title("Preservar bateria")
    root.attributes("-topmost", True)
    root.resizable(False, False)

    # Bloqueia o botão X e o Alt+F4
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
        # Carregador removido (ou sem bateria): fecha a janela
        if bateria is None or not bateria.power_plugged:
            root.destroy()
            return
        atualizar_texto(bateria.percent)
        root.after(1000, checar)  # checa de novo em 1 segundo

    atualizar_texto(percent)
    root.after(1000, checar)

    # Centraliza a janela na tela
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

        # PC sem bateria (desktop): encerra
        if bateria is None:
            break

        if not bateria.power_plugged:
            # Carregador removido: reinicia o ciclo
            continuar_ate_100 = False

        elif bateria.percent >= LIMITE and not continuar_ate_100:
            # Fica preso aqui até desplugar ou clicar em "Continuar"
            if aviso(bateria.percent):
                continuar_ate_100 = True

        time.sleep(INTERVALO)


if __name__ == "__main__":
    main()