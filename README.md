<div align="center">

# 🔋 Battery Alert

**Preserve a vida útil da bateria do seu notebook com um lembrete simples e persistente.**

![Plataforma](https://img.shields.io/badge/plataforma-Windows-0078D6?logo=windows&logoColor=white)
![Python](https://img.shields.io/badge/python-3.8%2B-3776AB?logo=python&logoColor=white)
![Licença](https://img.shields.io/badge/licença-MIT-green)
![Release](https://img.shields.io/github/v/release/Markhtus/CheckBattery)

</div>

---

## 📖 Sobre o projeto

baterias de íon-lítio duram mais quando evitam ficar muito tempo em 100% de carga. Muitos notebooks trazem uma opção de BIOS ou software do fabricante para limitar a carga em 80%, mas nem todos têm esse recurso.

O **Aviso de bateria** é um programa leve para Windows que roda em segundo plano e, quando a bateria atinge o limite configurado (padrão: **80%**), exibe uma janela pedindo para remover o carregador. A janela **só fecha quando o carregador é desconectado**, ou quando o usuário opta por carregar até 100%.

> ℹ️ O programa **avisa**, mas não corta a carga sozinho. Quem remove o carregador é o usuário.

## ✨ Funcionalidades

- 🔔 Aviso automático quando a bateria atinge o limite definido
- 🪟 Janela sempre na frente, com botão de fechar (X) e Alt+F4 bloqueados
- ⚡ A janela fecha sozinha assim que o carregador é removido
- 📊 Porcentagem atualizada em tempo real enquanto o aviso está aberto
- ✅ Botão **"Continuar carregando até 100%"** para quando for realmente necessário
- 🔄 Ciclo reiniciado automaticamente ao desplugar e plugar novamente
- 🚀 Inicia junto com o Windows
- 📦 Distribuído como `.exe`: **não precisa instalar Python** no notebook

## 🧠 Como funciona

```
Carregador conectado?
        │
        ├── Não ──► reinicia o ciclo e continua monitorando
        │
        └── Sim ──► bateria ≥ limite?
                        │
                        ├── Não ──► continua monitorando
                        │
                        └── Sim ──► mostra o aviso
                                      │
                                      ├── Usuário remove o carregador ──► janela fecha
                                      └── Usuário clica em "Continuar"  ──► janela fecha
                                                                           (sem novos avisos até
                                                                            desplugar e plugar de novo)
```

## 📥 Instalação (usuário final)

Não é necessário ter Python instalado.

1. Acesse a página de [**Releases**](https://github.com/Markhtus/CheckBattery/releases) e baixe o `baterry.exe` da versão mais recente.
2. Copie o arquivo para uma pasta fixa, por exemplo `C:\Programas\baterry\`.
3. Para iniciar junto com o Windows:
   1. Pressione `Win + R`, digite `shell:startup` e dê Enter.
   2. Clique com o botão direito no `baterry.exe` > **Criar atalho**.
   3. Mova o atalho para a pasta que abriu.
4. Reinicie o notebook (ou execute o `.exe` uma vez) e pronto.

> ⚠️ **Aviso do Windows:** como o executável não é assinado digitalmente, o SmartScreen ou o Defender podem exibir um alerta. Clique em **Mais informações > Executar assim mesmo**. O código-fonte está todo neste repositório para consulta.

### Conferir se está rodando

Abra o Gerenciador de Tarefas (`Ctrl + Shift + Esc`) e procure por `baterry.exe` na aba **Processos** ou **Detalhes**.

### Desinstalar

1. Finalize o `baterry.exe` pelo Gerenciador de Tarefas.
2. Apague o atalho da pasta `shell:startup`.
3. Apague o arquivo `baterry.exe`.

## ⚙️ Configuração

Os valores padrão são:

| Parâmetro   | Padrão | Descrição                                      |
|-------------|--------|------------------------------------------------|
| `LIMITE`    | `80`   | Porcentagem da bateria que dispara o aviso     |
| `INTERVALO` | `30`   | Segundos entre cada checagem da bateria        |

Para alterar os valores de forma permanente, edite as constantes no início do `baterry.py` e gere o executável novamente.

Para **testar** sem editar o código, passe os valores na linha de comando:

```
python baterry.py <LIMITE> <INTERVALO>
```

Exemplo, avisando a partir de 60% e checando a cada 5 segundos:

```
python baterry.py 60 5
```

## 🛠️ Rodando pelo código-fonte (desenvolvimento)

**Requisitos:** Windows e Python 3.8 ou superior.

```
git clone https://github.com/Markhtus/CheckBattery.git
cd CheckBattery

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt
python battery.py
```

> No PowerShell, ative o ambiente com `venv\Scripts\Activate.ps1`. Se aparecer erro de política de execução, rode uma vez `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`.

### Roteiro de testes

Com o carregador conectado e um limite abaixo da porcentagem atual (ex.: `python battery.py 60 5`):

- [ ] A janela aparece e **não** fecha com o X nem com Alt+F4
- [ ] A porcentagem exibida atualiza sozinha
- [ ] Ao remover o carregador, a janela fecha em até 1 segundo
- [ ] Ao plugar de novo (ainda acima do limite), a janela volta
- [ ] O botão "Continuar carregando até 100%" fecha a janela e ela não reaparece até desplugar
- [ ] Com o carregador removido, nada é exibido

## 📦 Gerando o executável

Com o ambiente virtual ativo:

```
pyinstaller --onefile --noconsole baterry.py
```

O arquivo será criado em `dist\baterry.exe`.

- `--onefile` gera um único arquivo.
- `--noconsole` evita abrir uma janela de terminal.

Para publicar: no GitHub, vá em **Releases > Draft a new release**, crie a tag (ex.: `v1.0`) e anexe o `baterry.exe`.

## 🗂️ Estrutura do projeto

```
CheckBattery/
├── battery.py          # código-fonte principal
├── requirements.txt    # dependências (psutil e pyinstaller)
├── .gitignore
├── LICENSE
└── README.md
```

As pastas `venv/`, `build/` e `dist/` e o arquivo `.spec` são gerados localmente e ficam fora do repositório.

## ❓ Perguntas frequentes

**O programa desliga o carregador sozinho?**
Não. Ele apenas avisa. Para limitar a carga em hardware, é preciso um recurso da BIOS ou do software do fabricante (Lenovo Vantage, ASUS Battery Health Charging, Dell Power Manager, etc.).

**Dá para fechar a janela sem desplugar?**
Pelo X ou Alt+F4, não. As opções são desplugar o carregador ou clicar em "Continuar carregando até 100%". Como último recurso, é possível finalizar o processo pelo Gerenciador de Tarefas.

**Funciona em Linux ou macOS?**
O código usa apenas `psutil` e `tkinter`, então deve rodar em outros sistemas, mas foi pensado e testado para Windows, e as instruções de inicialização automática são específicas dele.

**Funciona em PC desktop?**
Não. Sem bateria, o programa detecta isso e encerra sozinho.

**O programa consome muitos recursos?**
Muito pouco. Ele só consulta o estado da baterry a cada `INTERVALO` segundos.

**O antivírus bloqueou o arquivo. E agora?**
Executáveis gerados com PyInstaller costumam gerar falsos positivos. Você pode adicionar a pasta às exceções do antivírus ou gerar o `.exe` você mesmo a partir do código-fonte.

## 🧰 Tecnologias

- [Python](https://www.python.org/)
- [psutil](https://github.com/giampaolo/psutil): leitura do estado da bateria
- [tkinter](https://docs.python.org/3/library/tkinter.html): interface da janela de aviso
- [PyInstaller](https://pyinstaller.org/): geração do executável

## 🤝 Contribuindo

Sugestões e melhorias são bem-vindas:

1. Faça um fork do projeto
2. Crie uma branch: `git checkout -b minha-melhoria`
3. Commit: `git commit -m "Descreve a melhoria"`
4. Push: `git push origin minha-melhoria`
5. Abra um Pull Request

### Ideias para o futuro

- [ ] Aviso de bateria baixa (ex.: 20%)
- [ ] Alerta sonoro
- [ ] Ícone na bandeja do sistema
- [ ] Arquivo de configuração para alterar o limite sem recompilar
- [ ] Build automático do `.exe` com GitHub Actions

## 📄 Licença

Distribuído sob a licença MIT. Veja o arquivo `LICENSE` para mais informações.

---

<div align="center">

Feito com 🔋 para deixar a bataria viver mais.

</div>