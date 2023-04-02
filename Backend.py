import mysql.connector
from mysql.connector import Error

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
    query = mostra_articoli_utente + utente
    articoli = read_query(connection, query)
    return articoli

connection = create_db_connection("localhost", "root", "", "carrello atroos")

inserimento_ordini = """
INSERT INTO orders(ID, Utente, Stato) VALUES 
(1, 1, 'Pending');
"""

inserimento_utenti = """
INSERT INTO users(Nome, Cognome, CF) VALUES
('Marco', 'Zennaro', 'ZNNMRC01E07L736W'),
('Elia', 'Corò', 'CROLEI02C29L736W');
"""

inserimento_articoli_in_ordini = """
INSERT INTO contiene(Ordine, Articolo, Quantità) VALUES
(1, 'Pasta', 5);
"""

svuota = """
DELETE 
FROM users
"""

mostra_tutto = """
SELECT * 
FROM contiene 
"""

mostra_ordine = """
SELECT orders.ID 
FROM orders NATURAL JOIN users"""

mostra_articoli_utente = """
SELECT Nome, Prezzo, Quantità 
FROM articles INNER JOIN contiene on articles.Nome = contiene.Articolo 
INNER JOIN orders on orders.ID = contiene.Ordine
WHERE orders.Stato = 'Pending' and orders.Utente = """

#execute_query(connection, inserimento_articoli_in_ordini)
#results = read_query(connection, mostra_tutto)
#for result in results:
#    print(result)

articoli_ordine = mostra_articoli_carrello('1', mostra_articoli_utente)
for articolo in articoli_ordine:
    print(articolo[0], end=' ')
    print(articolo[1], end=' ')
    print(articolo[2])