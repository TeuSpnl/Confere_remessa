import PyPDF2
import re
import datetime
import os
import tkinter as tk
from tkinter.filedialog import askopenfilename


def log(msg):
    """   Gera um arquivo txt mostrando a mensagem que o programa passou na chamada    """

    # Define a data de hoje
    today = datetime.datetime.now()
    try:
        # Abre o arquivo pra editá-lo
        log = open(
            f"remessa/resultado_remessa-{today.strftime('%d-%m-%Y')}.txt", 'at+', encoding='utf-8')

    except (FileNotFoundError):  # Tenta criar o arquivo caso ele não exista
        try:
            log = open(
                f"remessa/resultado_remessa-{today.strftime('%d-%m-%Y')}.txt", 'at', encoding='utf-8')

        except (FileNotFoundError):  # Cria a pasta remessa, caso ela não exista
            os.mkdir('./remessa')
            log = open(
                f"remessa/resultado_remessa-{today.strftime('%d-%m-%Y')}.txt", 'at', encoding='utf-8')

        except Exception as e:
            print(f"Erro ao criar pasta do log!\nErro: {e.__class__}")

    except Exception as e:
        print(text=f"Erro ao criar log!\nErro: {e.__class__}")

    log.write(f"{msg}\n\n")


def extract_data_pdf(text):
    """ Função para extrair dados no formato "xxxxx/xxxx" de uma string """

    result = re.findall(r'\d+/\w', text)

    # for i in range(len(result)):
    #     result_novo = [item for item in result if item[-1].isalpha() == 1]
    result_novo = result.copy()

    for item in result:
        if item[-1].isalpha() == 0:
            result_novo.remove(item)

    return result_novo


def select_pdf():
    """ Função para selecionar o arquivo PDF e extrair os dados """

    try:
        # Abre o arquivo PDF a ser analizado
        file = askopenfilename(title="Selecione o PDF")
        file_pdf = open(file, 'rb')
        read_pdf = PyPDF2.PdfReader(file_pdf)

        # Conta o número de páginas que o PDF tem
        n = len(read_pdf.pages)
    except Exception as e:
        msg['text'] = f"Erro ao abrir o PDF!"
        return

    # O sistema pega os números dos boletos de cada página do PDF e adiona na lista
    for page_num in range(len(read_pdf.pages)):
        page = read_pdf.pages[page_num]
        page_text = page.extract_text()

        # Chama a função para todos os números
        data = extract_data_pdf(page_text)

        # Adiciona os números dos boletos na lista
        pdf.extend(data)

    # Fecha o arquivo PDF
    file_pdf.close()

    msg['text'] = "PDF carregado com sucesso!"


def select_txt():
    """ Função para selecionar o arquivo TXT e extrair os dados """
    try:
        # Abre o arquivo TXT a ser analizado
        file = askopenfilename(title="Selecione a remessa: ")
        with open(file, 'r') as file_txt:
            read_txt = file_txt.read()
    except Exception as e:
        msg['text'] = f"Erro ao abrir a remessa!"
        return

    # Encontrar os dados no arquivo TXT que estão após '71122'
    start_index = read_txt.find(pattern) + pattern.__len__()

    while start_index != pattern.__len__() - 1:
        # Encontrar o próximo '/' após o padrão
        slash_index = read_txt.find('/', start_index)

        if slash_index != -1:
            # Extrair o dado no formato "xxxxx/xxxx" e adicioná-lo à lista
            txt.append(read_txt[start_index:slash_index + 2])

            # Encontrar os dados no arquivo TXT que estão após '71122'
            start_index = read_txt.find(
                pattern, slash_index) + pattern.__len__()
        else:
            break

    msg['text'] = "Remessa carregada com sucesso!"


def confere():
    """ Função para compara os dados do PDF com os dados do TXT """

    # Impede que o sistema compare os dados caso os arquivos não tenham sido carregados
    while txt == [] or pdf == []:
        msg['text'] = "Carregue os arquivos primeiro!"
        return

    try:
        # Adiciona lembrete no log
        log("* LEMBRETE *\nSe faltar no PDF, é URGENTE.\nSe faltar no TXT, provavelmente são os LQ/BX, mas é necessário conferir.")

        log("‼‼‼‼ PDF ‼‼‼‼\n")
        # Verifica se os dados do TXT estão no PDF
        for data in txt:
            if data not in pdf:
                log(f'Falta o "{data}" no PDF.')

        log("\n‼‼‼‼ PDF ‼‼‼‼\n")

        log("\n#### TXT ####\n")
        # Verificar se os dados do PDF estão no TXT
        for data in pdf:
            if data not in txt:
                log(f'Falta o "{data}" no TXT.')

        log("\n#### TXT ####")

        msg['text'] = "Conferência finalizada com sucesso e registrada na PASTA REMESSA"
    except Exception as e:
        msg['text'] = f"Erro ao conferir os dados!\nErro: {e.__class__}"


def sel():
    """ Função para selecionar o layout da remessa """
    global pattern

    pattern_tk.set("71122" if cnab.get() == 0 else "1701")
    msg["text"] = f"Selecionado o layout {pattern_tk.get()}"
    pattern = pattern_tk.get()


# Cria a lista de número dos boletos
pdf = []

# Cria a lista de número dos boletos
txt = []


# Configs da janela
janela = tk.Tk()
janela.title("Conferência de Remessa")


# Título principal
mainTitle = tk.Label(text="Conferência de remessa", font=("Roboto, 35")).grid(
    row=0, column=0, sticky="NSEW", padx=50, pady=20, columnspan=5)

# Selecionar o layout de remessa
mainTitle = tk.Label(text="Layout da remessa", font=("Roboto, 14")).grid(
    row=1, column=0, sticky="NSEW", padx=15, pady=5, columnspan=5)

# Var de layout - inclusive o padrão de busca no TXT
cnab = tk.IntVar()
pattern_tk = tk.StringVar()
pattern = ""
# pattern = '1701'
# pattern = '71122'

R1 = tk.Radiobutton(text="CNAB 240", variable=cnab, value=0, command=sel)
R1.grid(sticky='W', row=2, column=0, padx=100, pady=10)

R2 = tk.Radiobutton(text="CNAB 400", variable=cnab, value=1, command=sel)
R2.grid(sticky='E', row=2, column=1, pady=10)

# Espaço
space0 = tk.Label(text=" ", font="Roboto, 12")
space0.grid(row=3, column=0, sticky="NSEW", columnspan=5, pady=(0, 5))

# Selecionar o PDF
subTitle1 = tk.Label(text="Selecione o pdf", anchor="w", padx=15, font=(
    "Roboto, 14")).grid(row=4, column=0, sticky="NSEW")

botaoBuscaPdf = tk.Button(text="Buscar", command=select_pdf, width=10, font="Roboto, 11").grid(
    column=1, row=4, columnspan=6, sticky="NW")

# Espaço
space1 = tk.Label(text="", font="Roboto, 12")
space1.grid(row=5, column=0, sticky="NSEW", columnspan=5, pady=(5, 10))

# Selecionar a remessa
subTitle2 = tk.Label(text="Selecione a remessa", anchor="w", padx=15, font=(
    "Roboto, 14")).grid(row=6, column=0, sticky="NSEW")

botaoBuscaTxt = tk.Button(text="Buscar", command=select_txt, width=10, font="Roboto, 11").grid(
    column=1, row=6, columnspan=6, sticky="NW")

# Espaço
space2 = tk.Label(text="", font="Roboto, 12")
space2.grid(row=7, column=0, sticky="NSEW", columnspan=5, pady=(5, 40))

# Botão de conferir
botaoConfere = tk.Button(text="Conferir", command=confere, width=10, font="Roboto, 11").grid(
    column=0, row=8, columnspan=5, sticky="NSEW", padx=20)

msg = tk.Label(text="", font="Roboto, 12")
msg.grid(row=12, column=0, sticky="NSEW", columnspan=5, pady=(25, 40))

janela.mainloop()

# SDG
# VIVA CRISTO REI!
