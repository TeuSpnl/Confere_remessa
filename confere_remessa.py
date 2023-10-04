import PyPDF2
import re
from tkinter.filedialog import askopenfilename
import datetime
import os


def log(msg):
    """   Gera um arquivo txt mostrando a mensagem que o programa passou na chamada    """

    # Define a data de hoje
    today = datetime.datetime.now()
    try:
        # Abre o arquivo pra editá-lo
        log = open(
            f"remessa/resultado_remessa.txt-{today.strftime('%d-%m-%Y')}", 'at+', encoding='utf-8')

    except (FileNotFoundError):  # Tenta criar o arquivo caso ele não exista
        try:
            log = open(
                f"remessa/resultado_remessa.txt-{today.strftime('%d-%m-%Y')}", 'at', encoding='utf-8')

        except (FileNotFoundError):  # Cria a pasta remessa, caso ela não exista
            os.mkdir('./remessa')
            log = open(
                f"remessa/resultado_remessa.txt-{today.strftime('%d-%m-%Y')}", 'at', encoding='utf-8')

        except Exception as e:
            print(f"Erro ao criar pasta do log!\nErro: {e.__class__}")

    except Exception as e:
        print(text=f"Erro ao criar log!\nErro: {e.__class__}")

    log.write(f"{msg}\n\n")


def extract_data_pdf(text):
    '''Função para extrair dados no formato "xxxxx/xxxx" de uma string'''
    result = re.findall(r'\d+/\w', text)

    for i in range(len(result)):
        result_novo = [item for item in result if item[-1].isalpha() == 1]

    return result_novo


# Abre o arquivo PDF a ser analizado
file = askopenfilename(title="Selecione o PDF")
file_pdf = open(file, 'rb')
read_pdf = PyPDF2.PdfReader(file_pdf)

# Conta o número de páginas que o PDF tem
n = len(read_pdf.pages)


# Cria a lista de número dos boletos
pdf = []

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

# Abre o arquivo TXT a ser analizado
file = askopenfilename(title="Selecione o REM")
with open(file, 'r') as file_txt:
    read_txt = file_txt.read()

# Cria a lista de número dos boletos e seta o padrão de busca
txt = []
pattern = '71122'

# Encontrar os dados no arquivo TXT que estão após '71122'
start_index = read_txt.find(pattern) + 5

while start_index != 4:
    # Encontrar o próximo '/' após o padrão
    slash_index = read_txt.find('/', start_index)

    if slash_index != -1:
        # Extrair o dado no formato "xxxxx/xxxx" e adicioná-lo à lista
        txt.append(read_txt[start_index:slash_index + 2])

        # Encontrar os dados no arquivo TXT que estão após '71122'
        start_index = read_txt.find(pattern, slash_index) + 5
    else:
        break

#Adiciona lembrete no log    
log("* LEMBRETE *\nSe faltar no PDF, é URGENTE.\nSe faltar no TXT, provavelmente são os LQ/BX, mas é necessário conferir.")


log("‼‼‼‼ PDF ‼‼‼‼\n")
# Verificar se os dados do TXT estão no PDF e vice-versa
for data in txt:
    if data not in pdf:
        log(f'Falta o "{data}" no PDF.')

log("\n‼‼‼‼ PDF ‼‼‼‼\n")

log("\n#### TXT ####\n")
# Verificar se os dados do PDF estão no TXT e vice-versa
for data in pdf:
    if data not in txt:
        log(f'Falta o "{data}" no TXT.')

log("\n#### TXT ####")

# SDG
# VIVA CRISTO REI!