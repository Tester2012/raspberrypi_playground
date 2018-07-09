import sys
import Adafruit_DHT
import time
import matplotlib.pyplot as plt

# Parse command line parameters.
sensor_args = { '11': Adafruit_DHT.DHT11,
                '22': Adafruit_DHT.DHT22,
                '2302': Adafruit_DHT.AM2302 }
if len(sys.argv) == 3 and sys.argv[1] in sensor_args:
    sensor = sensor_args[sys.argv[1]]
    pin = sys.argv[2]
else:
    sensor = Adafruit_DHT.DHT11
    pin = 4
    print('Picking default configuration...')
    print('sensor : ' + str(sensor) + ', pin : ' + str(pin))

i = 0
plt.show()
while True:
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

    if humidity is not None and temperature is not None:
        humidity = round(humidity, 1)
        temperature = round(temperature, 1)
        print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
        plt.ylim(0, 100)
        plt.subplot(1, 2, 1).scatter(i, humidity)
        plt.ylim(-273, 100)
        plt.subplot(1, 2, 2).scatter(i, temperature)
        plt.draw()
        plt.pause(1)
        i += 1
    else:
        print('Failed to get reading. Try again!')

    time.sleep(1)
