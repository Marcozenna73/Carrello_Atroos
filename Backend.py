import json
import mysql.connector
from mysql.connector import Error
from flask import Flask, render_template, redirect, request
app = Flask(__name__)

def create_db_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")
    return connection

def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")

def read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as err:
        print(f"Error: '{err}'")

def mostra_articoli_carrello(utente, mostra_articoli_utente):
    query = mostra_articoli_utente + str(utente)
    articoli = read_query(connection, query)
    return articoli

def acquista_articoli(utente, art_ord):
    acquista_art1 = """
    UPDATE articles 
    SET Quantita_disponibile = """
    acquista_art2 = """ 
    WHERE Nome = '"""
    effettua_ord = """
    UPDATE orders 
    SET Stato = 'Settled' 
    WHERE Utente = """
    for art in art_ord:
        quantita_art = art[3] - art[2]
        query_acquisto = acquista_art1 + str(quantita_art) + acquista_art2 + art[0] + "'"
        print(query_acquisto)
        execute_query(connection, query_acquisto)
    query_ordine = effettua_ord + str(utente)
    print(query_ordine)
    execute_query(connection, query_ordine)

def svuotaCarr(utente):
    trova_ordine = """
    SELECT ID 
    FROM orders 
    WHERE Stato = 'Pending' and Utente = """ + str(utente)
    ordine = read_query(connection, trova_ordine)
    query_svuota = svuota_car + str(ordine[0][0])
    print(query_svuota)
    execute_query(connection, query_svuota)

def aggiungiArt(nomeArt, utente):
    trova_ordine = """
    SELECT ID 
    FROM orders 
    WHERE Stato = 'Pending' and Utente = """ + str(utente)
    ordine = read_query(connection, trova_ordine)
    if(len(ordine) == 0):
        ultimo_ordine = """
        SELECT MAX(ID) 
        FROM orders"""
        ordine = read_query(connection, ultimo_ordine)
        nuovo_ordine = """
        INSERT INTO orders(ID, Utente, Stato) VALUES 
        (""" + str(ordine[0][0] + 1) + """, """ + str(utente) + """, 'Pending');"""
        execute_query(connection, nuovo_ordine)
        ordine = read_query(connection, trova_ordine)
    aggiungi = """
    INSERT INTO contiene(Ordine, Articolo, Quantità) VALUES 
    (""" + str(ordine[0][0]) + """, '""" + nomeArt + """', 1);"""
    print(aggiungi)
    execute_query(connection, aggiungi)

def cambiaQuant(nomeArt, quantita, utente):
    trova_ordine = """
    SELECT ID 
    FROM orders 
    WHERE Stato = 'Pending' and Utente = """ + str(utente)
    ordine = read_query(connection, trova_ordine)
    cambiaQ = """
    UPDATE contiene 
    SET Quantità = """ + str(quantita) + """ 
    WHERE Articolo = '""" + nomeArt + """' and Ordine = """ + str(ordine[0][0])
    print(cambiaQ)
    execute_query(connection, cambiaQ)

def rimuoviArt(nome):
    rimuovi = """
    DELETE 
    FROM contiene 
    WHERE Articolo = '""" + nome + "'"
    execute_query(connection, rimuovi)

connection = create_db_connection("localhost", "root", "", "carrello atroos")

inserimento_ordini = """
INSERT INTO orders(ID, Utente, Stato) VALUES 
(1, 1, 'Pending');"""

inserimento_utenti = """
INSERT INTO users(Nome, Cognome, CF) VALUES
('Marco', 'Zennaro', 'ZNNMRC01E07L736W'),
('Mario', 'Rossi', 'RSSMRA03C03L736W');"""

inserimento_articoli_in_ordini = """
INSERT INTO contiene(Ordine, Articolo, Quantità) VALUES
(1, 'Pasta', 5),
(1, 'Pizza', 3),
(1, 'Pane', 7);"""

svuota_car = """
DELETE 
FROM contiene
WHERE Ordine = """

mostra_contiene = """
SELECT * 
FROM contiene """

mostra_articoli = """
SELECT Nome, Prezzo, Foto 
FROM articles"""

mostra_ordine = """
SELECT orders.ID 
FROM orders NATURAL JOIN users"""

mostra_articoli_utente = """
SELECT Nome, Prezzo, Quantità, Quantita_disponibile, Foto 
FROM articles INNER JOIN contiene on articles.Nome = contiene.Articolo 
INNER JOIN orders on orders.ID = contiene.Ordine
WHERE orders.Stato = 'Pending' and orders.Utente = """

mostra_utenti = """
SELECT Nome 
FROM users """

numero_ordine = 1
ID_utente = 1

articoli_ordine = mostra_articoli_carrello(ID_utente, mostra_articoli_utente)
totale_ordine = 0
for articolo in articoli_ordine:
    totale_ordine += articolo[1]*articolo[2]
    print(articolo[0], end=' ')
    print(articolo[1], end=' ')
    print(articolo[2], end=' ')
    print(articolo[3])

numero_art_ord = len(articoli_ordine)
articoli_negozio = read_query(connection, mostra_articoli)
utenti_db = read_query(connection, mostra_utenti)

@app.route('/')
def Home():
   return render_template('PaginaHome.html', articoli = articoli_negozio, utenti = utenti_db)

@app.route('/Carrello')
def Carrello():
    articoli_ordine = mostra_articoli_carrello(ID_utente, mostra_articoli_utente)
    totale_ordine = 0
    for articolo in articoli_ordine:
        totale_ordine += articolo[1]*articolo[2]
    numero_art_ord = len(articoli_ordine)
    return render_template('PaginaCarrello.html', num_art_ord = numero_art_ord, articoli_ord = articoli_ordine, totale = totale_ordine, utenti = utenti_db)

@app.route('/acquista')
def acquista():
    articoli_ordine = mostra_articoli_carrello(ID_utente, mostra_articoli_utente)
    for articolo in articoli_ordine:
        if(articolo[2] >= articolo[3]):
            return Carrello()
    acquista_articoli(ID_utente, articoli_ordine)
    return Carrello()

@app.route('/svuotaCarrello')
def svuotaCarrello():
    svuotaCarr(ID_utente)
    return Carrello()

@app.route('/<nomeArt>/aggiungiArticolo')
def aggiungiArticolo(nomeArt):
    aggiungiArt(nomeArt, ID_utente)
    return Carrello()

@app.route('/<nomeArt>/<int:quantita>/cambiaQuantita')
def cambiaQuantita(nomeArt, quantita):
    cambiaQuant(nomeArt, quantita, ID_utente)
    return Carrello()

@app.route('/<nome_art>/rimuoviArticolo')
def rimuoviArticolo(nome_art):
    rimuoviArt(nome_art)
    return Carrello()
       
@app.route('/<user>/stampaUser')
def stampaUser(user):
    print(user)
    return Home()

#execute_query(connection, inserimento_articoli_in_ordini)

if __name__ == '__main__':
   app.run()