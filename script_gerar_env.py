# script_gerar_env.py

def criar_arquivo_env():
    conteudo = """EMAIL_REMETENTE=#########
SENHA_GMAIL=#######
HOST_SMTP=#########
PORTA_SMTP=###
"""
    with open(".env", "w", encoding="utf-8") as arquivo:
        arquivo.write(conteudo)
    print("Arquivo .env criado com sucesso!")

if __name__ == "__main__":
    criar_arquivo_env()