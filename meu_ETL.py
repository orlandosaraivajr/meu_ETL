from bs4 import BeautifulSoup
import requests
import sqlite3
from sqlite3 import OperationalError
from datetime import datetime
import csv


class Extract:
    header = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:32.0) Gecko/20100101 Firefox/32.0'}
    lista_fiis = []

    def __init__(self):
        pass

    def _extract_to_list(self):
        with open('fundosListados.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                self.lista_fiis.append(row['Codigo'])

    def get_lista_fiis(self):
        if len(self.lista_fiis) == 0:
            self._extract_to_list()
        return self.lista_fiis

    def get_cotacao(self, fii):
        fii = fii.replace('/fiis/', '')
        url = 'https://finance.yahoo.com/quote/' + fii + '11.SA'
        response = requests.get(url, headers=self.header)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'lxml')
            cotacao = soup.find_all('span', {"class": "Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)"})
            try:
                cotacao = cotacao[0].text
                print(fii + ' => ' + cotacao)
                return cotacao
            except IndexError:
                print(fii + ' não encontrado')
                cotacao = 0.0
                return cotacao

    def __str__(self):
        return "Classe Extract"

    def __repr__(self):
        return "Classe Extract"


class Loader:
    def __init__(self, nome_banco='fii.db'):
        self.nome_banco = nome_banco
        self._criar_banco_fii(self.nome_banco)

    def _criar_banco_fii(self, nome_banco):
        self.conn = sqlite3.connect(self.nome_banco)
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

    def armazenar_lista(self, lista_cotacao):
        self.conn = sqlite3.connect(self.nome_banco)
        self.cursor = self.conn.cursor()
        self.cursor.executemany("""
        INSERT INTO fii (codigo_fii, preco, datetime)
        VALUES (?,?,?)
        """, lista_cotacao)
        self.conn.commit()
        self.conn.close()

    def __str__(self):
        return "Classe Loader"

    def __repr__(self):
        return "Classe Loader"


class MeuETL:
    lista_cotacao = []
    lista_fiis = []

    def __init__(self, *args, **kwargs):
        self.extract = Extract()
        self.load = Loader()
        self.lista_fiis = self.extract.get_lista_fiis()

    def extract_transform(self):
        for fii in self.lista_fiis:
            cotacao = self.extract.get_cotacao(fii)
            self.lista_cotacao.append((fii, cotacao, datetime.now()))
        print(self.lista_cotacao)
        self.load.armazenar_lista(self.lista_cotacao)

    def __str__(self):
        return "Classe Transform"

    def __repr__(self):
        return "Classe Transform"


if __name__ == "__main__":
    meu_etl = MeuETL()
    meu_etl.extract_transform()
