import mysql.connector
from mysql.connector import Error
from flask import Flask, render_template
app = Flask(__name__)


#Definizioni funzioni
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


#Definizioni variabili
connection = create_db_connection("localhost", "root", "", "carrello atroos")

svuota_car = """
DELETE 
FROM contiene
WHERE Ordine = """

mostra_articoli = """
SELECT Nome, Prezzo, Foto 
FROM articles"""

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

numero_art_ord = len(articoli_ordine)
articoli_negozio = read_query(connection, mostra_articoli)
utenti_db = read_query(connection, mostra_utenti)


#Definizioni app route
@app.route('/')
def Home():
   num_utente = (ID_utente - 1)
   return render_template('PaginaHome.html', articoli = articoli_negozio, utenti = utenti_db, num_utente = num_utente)

@app.route('/Carrello')
def Carrello():
    articoli_ordine = mostra_articoli_carrello(ID_utente, mostra_articoli_utente)
    totale_ordine = 0
    for articolo in articoli_ordine:
        totale_ordine += articolo[1]*articolo[2]
    numero_art_ord = len(articoli_ordine)
    return render_template('PaginaCarrello.html', num_art_ord = numero_art_ord, articoli_ord = articoli_ordine, totale = totale_ordine, utenti = utenti_db, num_utente = (ID_utente - 1))

@app.route('/acquista')
def acquista():
    articoli_ordine = mostra_articoli_carrello(ID_utente, mostra_articoli_utente)
    for articolo in articoli_ordine:
        if(articolo[2] > articolo[3]):
            return Carrello()
    acquista_art1 = """
    UPDATE articles 
    SET Quantita_disponibile = """
    acquista_art2 = """ 
    WHERE Nome = '"""
    effettua_ord = """
    UPDATE orders 
    SET Stato = 'Settled' 
    WHERE Utente = """
    for art in articoli_ordine:
        quantita_art = art[3] - art[2]
        query_acquisto = acquista_art1 + str(quantita_art) + acquista_art2 + art[0] + "'"
        execute_query(connection, query_acquisto)
    query_ordine = effettua_ord + str(ID_utente)
    execute_query(connection, query_ordine)
    return Carrello()

@app.route('/svuotaCarrello')
def svuotaCarrello():
    trova_ordine = """
    SELECT ID 
    FROM orders 
    WHERE Stato = 'Pending' and Utente = """ + str(ID_utente)
    ordine = read_query(connection, trova_ordine)
    query_svuota = svuota_car + str(ordine[0][0])
    execute_query(connection, query_svuota)
    return Carrello()

@app.route('/<nomeArt>/aggiungiArticolo')
def aggiungiArticolo(nomeArt):
    trova_ordine = """
    SELECT ID 
    FROM orders 
    WHERE Stato = 'Pending' and Utente = """ + str(ID_utente)
    ordine = read_query(connection, trova_ordine)
    if(len(ordine) == 0):
        ultimo_ordine = """
        SELECT MAX(ID) 
        FROM orders"""
        ordine = read_query(connection, ultimo_ordine)
        nuovo_ordine = """
        INSERT INTO orders(ID, Utente, Stato) VALUES 
        (""" + str(ordine[0][0] + 1) + """, """ + str(ID_utente) + """, 'Pending');"""
        execute_query(connection, nuovo_ordine)
        ordine = read_query(connection, trova_ordine)
    aggiungi = """
    INSERT INTO contiene(Ordine, Articolo, Quantità) VALUES 
    (""" + str(ordine[0][0]) + """, '""" + nomeArt + """', 1);"""
    execute_query(connection, aggiungi)
    return Carrello()

@app.route('/<nomeArt>/<int:quantita>/cambiaQuantita')
def cambiaQuantita(nomeArt, quantita):
    trova_ordine = """
    SELECT ID 
    FROM orders 
    WHERE Stato = 'Pending' and Utente = """ + str(ID_utente)
    ordine = read_query(connection, trova_ordine)
    cambiaQ = """
    UPDATE contiene 
    SET Quantità = """ + str(quantita) + """ 
    WHERE Articolo = '""" + nomeArt + """' and Ordine = """ + str(ordine[0][0])
    execute_query(connection, cambiaQ)
    return Carrello()

@app.route('/<nome_art>/rimuoviArticolo')
def rimuoviArticolo(nome_art):
    rimuovi = """
    DELETE 
    FROM contiene 
    WHERE Articolo = '""" + nome_art + "'"
    execute_query(connection, rimuovi)
    return Carrello()
       
@app.route('/<user>/cambiaUtente')
def cambiaUtente(user):
    global ID_utente
    trova_ID_user = """
    SELECT ID 
    FROM users 
    WHERE Nome = '""" + user + "'"
    ID_user = read_query(connection, trova_ID_user)
    ID_utente = ID_user[0][0]
    return Home()

if __name__ == '__main__':
   app.run()