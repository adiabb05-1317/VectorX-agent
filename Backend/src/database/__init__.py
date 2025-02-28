import psycopg2
from psycopg2.pool import SimpleConnectionPool



class Database:
    def __init__(self):
        self.pool = SimpleConnectionPool(1, 20, user='postgres', password='', host='', port='5432', database='postgres')
         