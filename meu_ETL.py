from bs4 import BeautifulSoup 
import requests
import time
import sqlite3
from sqlite3 import OperationalError
from datetime import datetime
import csv

class MeuETL:
    def __init__(self, *args, **kwargs):  
        self.header = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:32.0) Gecko/20100101 Firefox/32.0'}
        self.lista_fiis = []
        with open('fundosListados.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                self.lista_fiis.append(row['Codigo'])


    def extract_transform(self):
        lista_cotacao = []
        for fii in self.lista_fiis:
            fii = fii.replace('/fiis/','')
            url = 'https://finance.yahoo.com/quote/' + fii + '11.SA'
            response = requests.get(url, headers=self.header)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'lxml')  
                cotacao = soup.find_all('span', {"class": "Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)"})
                try:
                    cotacao = cotacao[0].text
                    print(fii + ' => ' + cotacao)
                    lista_cotacao.append((fii, cotacao, datetime.now()))
                except IndexError:
                    print(fii + ' não encontrado')
        print(lista_cotacao)
        self.load(lista_cotacao)


    def load(self, lista_cotacao):
        self.criar_banco_fii()
        self.conn = sqlite3.connect('fii.db')
        self.cursor = self.conn.cursor()
    
        self.cursor.executemany("""
        INSERT INTO fii (codigo_fii, preco, datetime)
        VALUES (?,?,?)
        """, lista_cotacao)
        self.conn.commit()
        self.conn.close()         


    def criar_banco_fii(self):
        self.conn = sqlite3.connect('fii.db')
        self.cursor = self.conn.cursor()
        try:
            self.cursor.execute("""
                    CREATE TABLE fii (
                        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                        codigo_fii TEXT NOT NULL,
                        preco FLOAT NOT NULL,
                        datetime DATE NOT NULL );
                        """)
        except OperationalError:
            print('Tabela já criada')
        self.conn.close()


if __name__ == "__main__":
    meu_etl = MeuETL()
    meu_etl.extract_transform()





