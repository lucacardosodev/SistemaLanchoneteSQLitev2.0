import customtkinter as ctk
import sqlite3
import os
from tkinter import messagebox

ctk.set_appearance_mode('dark')
ctk.set_default_color_theme("blue")

def conectar():
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    caminho_banco = os.path.join(diretorio_atual, "sistema.db")

    conexao = sqlite3.connect(caminho_banco)
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS produtos (
            nome TEXT,
            preco REAL, 
            quantidade INTEGER
        )
    """)
    conexao.commit()
    return conexao, cursor

def consultar_produtos():
    conexao, cursor = conectar()
    cursor.execute("SELECT * FROM produtos ")
    itens = cursor.fetchall()
    conexao.close()

    # Habilita a caixa de texto para escrever e limpa o contéudo anterior
    caixa_resultados.configure(state="normal") 
    caixa_resultados.delete("1.0", "end")

    if not itens:
        caixa_resultados.insert("end", "Nenhum produto cadastrado até o momento.\n")
    else:
        caixa_resultados.insert("end", "-" * 55 + "\n")
        # Loop para escrever cada linha encontrada no banco dentro da caixa de texto.

        for linha in itens:
           # Usando a mesma f-string de formação do terminal
           texto = f"Produto {linha[0]:<15} | Preço R$ {linha[1]:>6.2f} | Estoque: {linha[2]}\n"
           caixa_resultados.insert("end", texto)
        
        # Bloqueia a caixa de texto para que o usuário não consiga apagar o texto gerado
        caixa_resultados.configure(state="disabled")

def cadastrar_produtos():
    nome = entry_nome.get().strip()
    preco_str = entry_preco.get().strip()
    quantidade_str = entry_quantidade.get().strip()

    if not nome:
        messagebox.showwarning("Aviso", "O nome do produto não pode ficar vazio! ")
        return

    try:
        preco = float(preco_str)
        quantidade = int(quantidade_str)

        conexao, cursor = conectar()
        cursor.execute("INSERT INTO produtos VALUES (?, ?, ?)", (nome, preco, quantidade))
        conexao.commit()
        conexao.close()

        messagebox.showinfo("Sucesso", f"Produto '{nome}' cadastrado!")

    except ValueError:
        messagebox.showerror("ERROR DE DIGITAÇÃO", "Digite valores númericos válidos!")

def encerrar_sistema():
    messagebox.showinfo("Encerrar sistema", "Sistema encerrando...")
    janela.destroy()

janela = ctk.CTk()
janela.title("Lanchonete Ennius Muniz - Senac-DF")
janela.geometry("600x650")

titulo = ctk.CTkLabel(janela, text = "=== SISTEMA DE CONTROLE (SQLite) ===", font=("Arial", 24))
titulo.pack(pady=20)

entry_nome = ctk.CTkEntry(janela, placeholder_text= "1. Nome do Produto", width=350)
entry_nome.pack(pady=20)

entry_preco = ctk.CTkEntry(janela, placeholder_text= "2. Preço (EX.: 5.00)", width=350)
entry_preco.pack(pady=20)

entry_quantidade = ctk.CTkEntry(janela, placeholder_text= "3. Quantidade em Estoque", width=350)
entry_quantidade.pack(pady=20)

btn_salvar = ctk.CTkButton(janela, text="Salvar Produto", fg_color="green", command=cadastrar_produtos)
btn_salvar.pack(pady=15)

btn_encerrar = ctk.CTkButton(janela, text="Encerrar Sistema", fg_color="red", command=encerrar_sistema)
btn_encerrar.pack(pady=15)

btn_consultar = ctk.CTkButton(janela, text="Consultar Produtos Salvos", command=consultar_produtos)
btn_consultar.pack(pady=20)

caixa_resultados = ctk.CTkTextbox(janela, width=450, height=200, font= ("Courier", 12))
caixa_resultados.pack(pady=20)
caixa_resultados.configure(state="disabled")

janela.mainloop()