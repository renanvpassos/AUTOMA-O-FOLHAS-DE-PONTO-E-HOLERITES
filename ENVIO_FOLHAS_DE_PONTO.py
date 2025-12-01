import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

# Carregar variáveis do .env
load_dotenv()
EMAIL_REMETENTE = os.getenv("EMAIL_REMETENTE")
SENHA = os.getenv("SENHA_GMAIL")

# Mês atual em português
meses_pt = [
    "JANEIRO", "FEVEREIRO", "MARÇO", "ABRIL", "MAIO", "JUNHO",
    "JULHO", "AGOSTO", "SETEMBRO", "OUTUBRO", "NOVEMBRO", "DEZEMBRO"
]
# Solicitar mês ao usuário
while True:
    entrada_mes = input("Digite o número do mês (1 a 12): ").strip()
    if entrada_mes.isdigit() and 1 <= int(entrada_mes) <= 12:
        mes_atual = meses_pt[int(entrada_mes) - 1]
        break
    else:
        print("Entrada inválida. Por favor, digite um número entre 1 e 12.")

# Funcionários e e-mails
funcionarios = {
    "DALILA TRINDADE": "renan.veloso@multprocessing.com.br",
    "JULIANA LAFACE": "renan.veloso@multprocessing.com.br",
    "LAISA SAMPAIO": "renan.veloso@multprocessing.com.br",
    "LARYSSA MORAIS": "renan.veloso@multprocessing.com.br",
    "LEONARDO SANTOS": "renan.veloso@multprocessing.com.br",
    "LUCAS SERRA": "renan.veloso@multprocessing.com.br",
    "LUCAS FERREIRA": "renan.veloso@multprocessing.com.br",
    "LUDMILA": "renan.veloso@multprocessing.com.br",
    "MIKAEL": "renan.veloso@multprocessing.com.br",
    "NATHALY": "renan.veloso@multprocessing.com.br",
    "RAIHANA": "renan.veloso@multprocessing.com.br",
    "PRISCILA": "renan.veloso@multprocessing.com.br",
}

arquivos_por_funcionario = {nome: [] for nome in funcionarios}
status_labels = {}

# Função para anexar arquivos
def anexar_arquivos(nome):
    arquivos = filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf")])
    if arquivos:
        arquivos_por_funcionario[nome].extend(arquivos)
        status_labels[nome].config(text="inserido", fg="green")
        messagebox.showinfo("Arquivos anexados", f"{len(arquivos)} arquivos adicionados para {nome}.")

# Função para enviar e-mails
def enviar_emails():
    if not messagebox.askyesno("Confirmação", "Deseja realmente enviar todos os e-mails?"):
        return

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL_REMETENTE, SENHA)

        for nome, email in funcionarios.items():
            if not arquivos_por_funcionario[nome]:
                continue

            msg = MIMEMultipart()
            msg["From"] = EMAIL_REMETENTE
            msg["To"] = email
            msg["Subject"] = f"FOLHAS DE PONTO - {mes_atual}"

            mensagem = f"""Olá!

Seguem folhas de ponto referentes ao mês de {mes_atual}

Att,"""
            msg.attach(MIMEText(mensagem, "plain"))

            for caminho in arquivos_por_funcionario[nome]:
                with open(caminho, "rb") as f:
                    part = MIMEApplication(f.read(), Name=os.path.basename(caminho))
                    part["Content-Disposition"] = f'attachment; filename="{os.path.basename(caminho)}"'
                    msg.attach(part)

            server.send_message(msg)

        server.quit()
        messagebox.showinfo("Sucesso", "Todos os e-mails foram enviados com sucesso!")

        # Atualizar botão após envio
        btn_enviar.config(
            text="✅ Folhas de Ponto Enviadas",
            bg="#3399ff",  # azul médio
            fg="white",
            state="disabled"  # 🔒 desativa o botão
        )

    except smtplib.SMTPAuthenticationError:
        messagebox.showerror("Erro de autenticação", "Verifique o e-mail e a senha.")
    except smtplib.SMTPConnectError:
        messagebox.showerror("Erro de conexão", "Não foi possível conectar ao servidor SMTP.")
    except Exception as e:
        messagebox.showerror("Erro", f"Falha ao enviar e-mails: {e}")

# Interface gráfica
root = tk.Tk()
root.title("CENTRAL DE ENVIOS DE FOLHA DE PONTO")
root.geometry("600x600")
root.configure(bg="#a3d9ff")
root.resizable(True, True)

# Label para imagem de fundo
bg_label = tk.Label(root)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# Carregar imagem original
caminho_imagem = "BACKGROUND_MULT_1920X1080.jpg"
imagem_original = None

try:
    if os.path.exists(caminho_imagem):
        imagem_original = Image.open(caminho_imagem)
    else:
        raise FileNotFoundError(f"Imagem não encontrada: {caminho_imagem}")
except Exception as e:
    print(f"Erro ao carregar imagem: {e}")
    imagem_original = None

# Redimensionar e aplicar imagem ao fundo
def atualizar_imagem_fundo(event=None):
    if imagem_original:
        largura = root.winfo_width()
        altura = root.winfo_height()
        imagem_redimensionada = imagem_original.resize((largura, altura), Image.LANCZOS)
        imagem_tk = ImageTk.PhotoImage(imagem_redimensionada)
        bg_label.configure(image=imagem_tk)
        bg_label.image = imagem_tk  # manter referência

# Atualizar imagem ao redimensionar
root.bind("<Configure>", atualizar_imagem_fundo)
root.after(100, atualizar_imagem_fundo)

# Frame para os botões
frame = tk.Frame(root, bg="#a3d9ff")
frame.pack(fill="x", padx=20, pady=(20, 0))

# Botões dos funcionários + status
for i, nome in enumerate(funcionarios):
    btn = tk.Button(frame, text=nome, command=lambda n=nome: anexar_arquivos(n),
                    font=("Comic Sans MS", 12), bg="#ffcc00", fg="black")
    btn.grid(row=i, column=0, sticky="ew", padx=10, pady=5)

    status = tk.Label(frame, text="", font=("Comic Sans MS", 10), bg="#a3d9ff", fg="green")
    status.grid(row=i, column=1, sticky="w", padx=5)
    status_labels[nome] = status

# Botão de envio
btn_enviar = tk.Button(frame, text="📤 Enviar Todos", command=enviar_emails,
                       font=("Comic Sans MS", 14, "bold"), bg="#00cc66", fg="white")
btn_enviar.grid(row=len(funcionarios), column=0, columnspan=2, sticky="ew", padx=10, pady=20)

frame.grid_columnconfigure(0, weight=1)

# Ajustar altura do frame
def ajustar_frame_altura(event):
    altura_total = root.winfo_height()
    frame.config(height=altura_total)

root.bind("<Configure>", ajustar_frame_altura)

root.mainloop()