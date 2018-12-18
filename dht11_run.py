import sys
import Adafruit_DHT
import time
from datetime import datetime
import sqlite3

# Parse command line parameters.
sensor_args = {'11': Adafruit_DHT.DHT11,
               '22': Adafruit_DHT.DHT22,
               '2302': Adafruit_DHT.AM2302}
if len(sys.argv) == 3 and sys.argv[1] in sensor_args:
    sensor = sensor_args[sys.argv[1]]
    pin = sys.argv[2]
else:
    sensor = Adafruit_DHT.DHT11
    pin = 4
    print('Picking default configuration...')
    print('sensor : ' + str(sensor) + ', pin : ' + str(pin))

with sqlite3.connect('dht11.db') as connection:
    connection.execute('''create table if not exists dht11_info (
                        id integer primary key autoincrement,
                        time integer,
                        temperature real,
                        humidity real
                      )''')

    while True:
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

        if humidity is not None and temperature is not None:
            humidity = round(humidity, 1)
            temperature = round(temperature, 1)
            current_time = datetime.now()

            print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
            connection.execute('insert into dht11_info(time, temperature, humidity) values(?, ?, ?)',
                               (current_time, temperature, humidity))
        else:
            print('Failed to get reading. Try again!')

        time.sleep(20)
