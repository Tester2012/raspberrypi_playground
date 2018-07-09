import sys
import Adafruit_DHT
import time
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import matplotlib.dates as mdates

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

plt.show()
figure = plt.figure()
ax = figure.add_subplot(2, 1, 1)
locs, labels = plt.xticks()
ax.xaxis.set_major_locator(mdates.HourLocator(interval=1))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
plt.setp(labels, rotation=90)

max_temperature = (-273, [datetime.now()])
annotations = list()

while True:
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

    if humidity is not None and temperature is not None:
        humidity = round(humidity, 1)
        temperature = round(temperature, 1)
        current_time = datetime.now()

        temperaturePlot = plt.subplot(2, 1, 1)
        plt.ylim([-273, 100])

        earliest_time = current_time - timedelta(day=1)
        plt.xlim([earliest_time, current_time])

        if max_temperature[0] < temperature:
            max_temperature = (temperature, [current_time])
            for annotation in annotations:
                annotation.remove()
            annotations.clear()
        elif max_temperature[0] == temperature:
            max_temperature[1].append(current_time)


        for xmax in max_temperature[1]:
            annotation = temperaturePlot.annotate("{:.1f}".format(max_temperature[0]),
                                          xy=(current_time, max_temperature[0]),
                                          xytext=(xmax, max_temperature[0] + 10),
                                          color = 'black',
                                          fontsize=12)
            annotations.append(annotation)

        print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))

        temperaturePlot.scatter(current_time, temperature)
        plt.draw()
        plt.pause(1)
    else:
        print('Failed to get reading. Try again!')

    time.sleep(59)
