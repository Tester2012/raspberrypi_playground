import sqlite3
from datetime import datetime

class DHT11DbHelper:

    def __init__(self, database_name = 'dht11.db', types = sqlite3.PARSE_DECLTYPES):
        self.database_name = database_name
        self.types = types
        self.connection = None
        print("__init__() called")

    # this is called when an object is created using "with"
    def __enter__(self):
        self.open_db()
        return self

    # # this is called when an object is out of "with"
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()

    # this method should not be exposed outside
    def __open_db(self):
        self.connection = sqlite3.connect(self.database_name, self.types)

        with self.connection:
            self.connection.execute('''create table if not exists dht11_info 
                (id integer primary key autoincrement, 
                temperature integer, 
                humidity integer, 
                measure_time timestamp);''')

    def insert(self, temperature, humidity):
        with self.connection:
            measure_time = datetime.now()
            self.connection.execute('insert into dht11_info(temperature, humidity, measure_time) '
                                    'values (?, ?, ?)',
                                    (temperature, humidity, measure_time,))

