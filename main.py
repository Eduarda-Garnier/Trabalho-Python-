import tkinter as tk
from tkinter import messagebox
import sqlite3


def criar_tabela():
    conn = sqlite3.connect('banco_dados.db')
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT NOT NULL,
            senha TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


def fazer_login():
    usuario = entry_usuario.get()
    senha = entry_senha.get()

    conn = sqlite3.connect('banco_dados.db')
    cur = conn.cursor()

    cur.execute("SELECT * FROM usuarios WHERE usuario = ? AND senha = ?", (usuario, senha))
    resultado = cur.fetchone()

    if resultado:
        messagebox.showinfo("Sucesso", "Login bem-sucedido!")
        abrir_janela_principal()
    else:
        messagebox.showerror("Erro", "Usuário ou senha inválidos!")

    conn.close()

def abrir_janela_principal():
    janela_login.destroy()  
    co1 = "#feffff"  # branca
    co2 = "#4fa882"  # verde
    co3 = "#38576b"  # valor
    co4 = "#403d3d"   # letra
    co6 = "#038cfc"   # azul
    co7 = "#ef5350"   # vermelha
    co8 = "#263238"   # verde escuro
    co9 = "#e9edf5"   # escuro azul
    co10 = "#808080"  # cinza
    co11 = "FFFF00" # amarelo

    from pickle import FALSE
    import tkinter as tk
    from tkinter import CENTER, NSEW, NW, ttk, messagebox
    
    from operacoes import inserirProduto, atualizarProduto, exibirProduto, deletarProduto


    janela = tk.Tk()
    janela.title("")
    janela.geometry('1043x453')
    janela.configure(background=co9)
    janela.resizable(False, False)

    frame_cima = tk.Frame(janela, width=400, height=50, background=co10, relief='flat')
    frame_cima.grid(row=0, column=0)

    app_nome = tk.Label(frame_cima, text="Cadastro de Produtos", anchor=NW, font=('Ivy 13 bold'), bg=co10, fg=co1, relief='flat')
    app_nome.place(x=10, y=20)

    frame_baixo = tk.Frame(janela, width=310, height=403, background=co1, relief='flat')
    frame_baixo.grid(row=1, column=0, sticky=NSEW, padx=0,pady=1)

    label_nome = tk.Label(frame_baixo, text="Nome", anchor=NW, font=('Ivy 10 bold'), bg=co1, fg=co4, relief='flat')
    label_nome.place(x=10, y=10)

    entry_nome = tk.Entry(frame_baixo, width=45, justify="left", relief='solid')
    entry_nome.place(x=10, y=40)

    label_codigo = tk.Label(frame_baixo, text="Codigo", anchor=NW, font=('Ivy 10 bold'), bg=co1, fg=co4, relief='flat')
    label_codigo.place(x=10, y=70)

    entry_codigo = tk.Entry(frame_baixo, width=45, justify="left", relief='solid')
    entry_codigo.place(x=10, y=100)

    label_quantiade = tk.Label(frame_baixo, text="Quantidade", anchor=NW, font=('Ivy 10 bold'), bg=co1, fg=co4, relief='flat')
    label_quantiade.place(x=10, y=130)

    entry_quantidade = tk.Entry(frame_baixo, width=45, justify="left", relief='solid')
    entry_quantidade.place(x=10, y=160)



    def inserir():
        global tree

        nome = entry_nome.get()
        codigo = entry_codigo.get()
        quantidade = entry_quantidade.get()
        

        lista = [nome, codigo, quantidade]

        if nome == "":
            messagebox.showerror('Erro', 'Nome está vazio')
        else:
            inserirProduto(lista)
            messagebox.showinfo('Sucesso', 'Os dados foram inseridos!!')

            entry_nome.delete(0,'end')
            entry_codigo.delete(0,'end')
            entry_quantidade.delete(0,'end')
            
        for widget in frame_direita.winfo_children():
            widget.destroy()
        
        exibir()

    def exibir():
        global tree

        lista = exibirProduto()

        tabela_head = ['ID','Nome', 'Código', 'Quantidade']


        tree = ttk.Treeview(frame_direita, selectmode="extended", columns=tabela_head, show="headings")

        vsb = ttk.Scrollbar(frame_direita, orient="vertical", command=tree.yview)

        hsb = ttk.Scrollbar( frame_direita, orient="horizontal", command=tree.xview)

        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        tree.grid(column=0, row=0, sticky='nsew')
        vsb.grid(column=1, row=0, sticky='ns')
        hsb.grid(column=0, row=1, sticky='ew')

        frame_direita.grid_rowconfigure(0, weight=12)


        hd=["nw","nw","nw","nw","nw","center","center"]
        h=[30,170,140,100,120,50,100]
        n=0

        for col in tabela_head:
            tree.heading(col, text=col.title(), anchor=CENTER)
            
            tree.column(col, width=h[n],anchor=hd[n])
            
            n+=1

        for item in lista:
            tree.insert('', 'end', values=item)

    def atualizar():
        global tree
        try:
            treev_dados = tree.focus()
            treev_dicionario = tree.item(treev_dados)
            tree_lista = treev_dicionario['values']

            valor_id = tree_lista[0]

            entry_nome.delete(0,'end')
            entry_codigo.delete(0,'end')
            entry_quantidade.delete(0,'end')
            
            entry_nome.insert(0, tree_lista[1])
            entry_codigo.insert(0, tree_lista[2])
            entry_quantidade.insert(0, tree_lista[3])
            
            def update():
                nome = entry_nome.get()
                codigo = entry_codigo.get()
                quantidade = entry_quantidade.get()
                

                lista = [nome, codigo, quantidade, valor_id]

                if nome == "":
                    messagebox.showerror('Erro', 'Nome está vazio')
                else:
                    atualizarProduto(lista)
                    messagebox.showinfo('Sucesso', 'Os dados foram atualizados!!')

                    entry_nome.delete(0,'end')
                    entry_codigo.delete(0,'end')
                    entry_quantidade.delete(0,'end')
                
                for widget in frame_direita.winfo_children():
                    widget.destroy()
                
            button_confirmar = tk.Button(frame_baixo, command=update, text="Confirmar", width=10, font=('Ivy 7 bold'), bg=co2, fg=co1, relief='raised', overrelief='ridge')
            button_confirmar.place(x=110, y=370)
                
            exibir()

        except IndexError:
            messagebox.showerror('Erro', 'Selecione um dos dados na tabela para atualizar')

    def deletar():
        global tree
        try:
            treev_dados = tree.focus()
            treev_dicionario = tree.item(treev_dados)
            tree_lista = treev_dicionario['values']

            valor_id = [tree_lista[0]]

            deletarProduto(valor_id)
            messagebox.showinfo('Sucesso', 'Dados deletados com sucesso')

            for widget in frame_direita.winfo_children():
                widget.destroy()


        except IndexError:
            messagebox.showerror('Erro', 'Selecione algum dado para deletar')


    button_inserir = tk.Button(frame_baixo, command=inserir, text="Inserir", width=10, font=('Ivy 9 bold'), bg=co6, fg=co1, relief='raised', overrelief='ridge')
    button_inserir.place(x=15, y=340)

    button_atualaizar = tk.Button(frame_baixo, command=atualizar, text="Atualizar", width=10, font=('Ivy 9 bold'), bg=co2, fg=co1, relief='raised', overrelief='ridge')
    button_atualaizar.place(x=110, y=340)

    button_deletar = tk.Button(frame_baixo, command=deletar, text="Deletar", width=10, font=('Ivy 9 bold'), bg=co7, fg=co1, relief='raised', overrelief='ridge')
    button_deletar.place(x=200, y=340)

    button_exibir = tk.Button(frame_baixo, text="Exibir", width=10, font=('Ivy 9 bold'), bg=co3, fg=co1, relief='raised', overrelief='ridge', command=exibir)
    button_exibir.place(x=290, y=340)

    frame_direita = tk.Frame(janela, width=643, height=403, background=co1, relief='flat')
    frame_direita.grid(row=0, column=1, rowspan=2, padx=1, pady=0, sticky=NSEW)



    janela.mainloop()




def abrir_tela_cadastro():
    janela_login.withdraw() 
    janela_cadastro = tk.Tk()
    janela_cadastro.title("Cadastro")
    janela_cadastro.geometry("300x200")

    label_usuario = tk.Label(janela_cadastro, text="Usuário:")
    label_usuario.pack()

    entry_usuario_cadastro = tk.Entry(janela_cadastro)
    entry_usuario_cadastro.pack()

    label_senha = tk.Label(janela_cadastro, text="Senha:")
    label_senha.pack()

    entry_senha_cadastro = tk.Entry(janela_cadastro, show="*")
    entry_senha_cadastro.pack()

    button_cadastrar = tk.Button(janela_cadastro, text="Cadastrar", command=lambda: cadastrar_usuario(entry_usuario_cadastro.get(), entry_senha_cadastro.get()))
    button_cadastrar.pack()

    def cadastrar_usuario(usuario, senha):
        conn = sqlite3.connect('banco_dados.db')
        cur = conn.cursor()

        cur.execute("INSERT INTO usuarios (usuario, senha) VALUES (?, ?)", (usuario, senha))
        conn.commit()

        messagebox.showinfo("Sucesso", "Cadastro concluído com sucesso!")

        conn.close()

        janela_cadastro.destroy() 
        janela_login.deiconify()  


criar_tabela()

janela_login = tk.Tk()
janela_login.title("Login")
janela_login.geometry("300x200")

label_usuario = tk.Label(janela_login, text="Usuário:")
label_usuario.pack()

entry_usuario = tk.Entry(janela_login)
entry_usuario.pack()

label_senha = tk.Label(janela_login, text="Senha:")
label_senha.pack()

entry_senha = tk.Entry(janela_login, show="*")
entry_senha.pack()

button_login = tk.Button(janela_login, text="Login", command=fazer_login)
button_login.pack()

button_cadastro = tk.Button(janela_login, text="Cadastro", command=abrir_tela_cadastro)
button_cadastro.pack()

janela_login.mainloop()