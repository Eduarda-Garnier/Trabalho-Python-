import sqlite3 as lite

con = lite.connect('dados.db')


def inserirProduto(i):
    with con:
        cur = con.cursor()
        query = "INSERT INTO formulario (nome, codigo, quantidade) VALUES (?, ?, ?)"
        cur.execute(query,i)



def exibirProduto():
    lista = []
    with con:
        cur = con.cursor()
        query = "SELECT * FROM formulario"
        cur.execute(query)
        produto = cur.fetchall()

        for i in produto:
            lista.append(i)
    return lista
    


def atualizarProduto(i):
    with con:
        cur = con.cursor()
        query = "UPDATE formulario SET nome=?, codigo=?, quantidade=? WHERE id=?"
        cur.execute(query,i)


def deletarProduto(i):
    with con:
        cur = con.cursor()
        query = "DELETE FROM formulario WHERE id=?"
        cur.execute(query, i)
