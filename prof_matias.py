import csv
import sqlite3 as sql
import json
import requests



def create_schema():
    
    conn = sql.connect('MERCADOlibre.db')

    c = conn.cursor()

    c.execute("""
                DROP TABLE IF EXISTS Datosmercado;
            """)

    c.execute("""
            CREATE TABLE Datosmercado(
                [id] TEXT PRIMARY KEY,
                [site_id] TEXT,
                [title] TEXT,
                [price] INTEGER,
                [currency_id] TEXT,
                [initial_quantity] INTEGER,
                [available_quantity] INTEGER,
                [sold_quantity] INTEGER
            );
            """)

    conn.commit()

    conn.close()
    
def fill():
    
    with open('meli_technical_challenge_data.csv', 'r') as archivo:
        data = list(csv.DictReader(archivo))
        #print(data)
        
        lista = []
        
        for i in data:
            x = i['site'] + i['id']
            lista.append(x)
        
        for s in lista:
            
            url = 'https://api.mercadolibre.com/items?ids='+s
            response = requests.get(url).json()
            data = response[0]['body']
            
            try:
                
            
                id1 = data["id"]
                site_id1 = data["site_id"]
                title1 = data["title"]
                price1 = data["price"]
                currency_id1 = data["currency_id"]
                initial_quantity1 = data["initial_quantity"]
                available_quantity1 = data["available_quantity"]
                sold_quantity1 = data["sold_quantity"]
            
                dataset = (id1, site_id1, title1, price1, currency_id1, initial_quantity1, available_quantity1, sold_quantity1)
            
                conn = sql.connect('MERCADOlibre.db')
                c = conn.cursor()
                c.execute("""INSERT INTO Datosmercado (id, site_id, title,price, currency_id, initial_quantity, available_quantity, sold_quantity )
                            VALUES (?,?,?,?,?,?,?,?);""", dataset)

            
                conn.commit()
            except:
                continue
        
        
        c.execute('SELECT * FROM Datosmercado')
    
        while True:
            row = c.fetchone()
                
            if row is None:
                break
            
            #print(row)

        conn.close()


def fetch():
    
    busqueda = 'MLA845041373'
    
    conn = sql.connect('MERCADOlibre.db')
    c = conn.cursor()
    
    try:
        c.execute('SELECT * FROM Datosmercado WHERE id =?', busqueda)
        busqueda_sucess = c.fetchone()
        print(busqueda_sucess)
    except:
        print('el id no existe')
        
            
            
            
            
            


            
        
if __name__ == "__main__":
    
    create_schema()
    fill()
    fetch()

