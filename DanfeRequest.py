import requests
import tkinter as tk
from tkinter import filedialog

def selecionar_arquivo():
    global xml_nfe
    xml_file_path = filedialog.askopenfilename(filetypes=[("Arquivos XML", "*.xml")])
    
    if xml_file_path:
        with open(xml_file_path, 'r', encoding='utf-8') as xml_file:
            xml_nfe = xml_file.read()
        
        label_arquivo.config(text=f"Arquivo selecionado: {xml_file_path}")

def enviar_requisicao():
    global xml_nfe
    if xml_nfe:
        # URL da API
        api_url = "https://ws.meudanfe.com/api/v1/get/nfe/xmltodanfepdf/API"

        headers = {
            'Content-Type': 'text/plain',
        }

        response = requests.post(api_url, headers=headers, data=xml_nfe)

        if response.status_code == 200:
            base64_response = response.text.strip('data:application/pdf;base64,').strip('"')

            file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("Arquivos PDF", "*.pdf")])
            if file_path:
                with open(file_path, 'wb') as pdf_file:
                    import base64
                    pdf_file.write(base64.b64decode(base64_response))

                resultado.config(text="PDF do DANFE salvo com sucesso.")
            else:
                resultado.config(text="Operação cancelada pelo usuário.")
        else:
            resultado.config(text="Falha ao gerar PDF do DANFE! Confira o seu XML.")
            resultado.config(f"Código de status HTTP: {response.status_code}")
    else:
        resultado.config(text="Selecione um arquivo XML antes de enviar a requisição.")

root = tk.Tk()
root.title("XML para DANFE")

largura = 500
altura = 100
largura_tela = root.winfo_screenwidth()
altura_tela = root.winfo_screenheight()
x = (largura_tela - largura) // 2
y = (altura_tela - altura) // 2
root.geometry(f"{largura}x{altura}+{x}+{y}")

selecionar_button = tk.Button(root, text="Carregar XML", command=selecionar_arquivo)
selecionar_button.pack()

label_arquivo = tk.Label(root, text="")
label_arquivo.pack()

enviar_button = tk.Button(root, text="Download", command=enviar_requisicao)
enviar_button.pack()

resultado = tk.Label(root, text="")
resultado.pack()

root.mainloop()
