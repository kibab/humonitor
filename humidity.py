import Adafruit_DHT
import datetime
import Adafruit_BMP.BMP085 as BMP085
from prometheus_client import start_http_server, Summary, Gauge

DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 7
baro_sensor = BMP085.BMP085(busnum=1)
hum_metric = Gauge('humidity', 'Current humidity')
pressure_metric = Gauge('pressure', 'Current pressure')
temp_metric = Gauge('temperature', 'Current temperature')

def do_work():
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    hum_metric.set(humidity)
    pressure = baro_sensor.read_pressure()
    pressure_metric.set(pressure)
    alt = baro_sensor.read_altitude()
    baro_temp = baro_sensor.read_temperature()
    temp_metric.set(baro_temp)
    print("Date = {0}, Temp = {1:0.1f}*C, Humidity = {2:0.1f}%, Pressure = {3:0.2f} Pa, Altitide = {4:0.2f} m, Barotemp = {5:0.1f}*C".format(datetime.datetime.now(), temperature, humidity, pressure, alt, baro_temp))
    #print("Temp = {0:0.2f} *C".format(baro_sensor.read_temperature()))
    #print("Pressure = {0:0.2f} Pa".format(baro_sensor.read_pressure()))
    #print("Altitude = {0:0.2f} m".format(baro_sensor.read_altitude()))
    #print("Sealevel Pressure = {0:0.2f} Pa".format(baro_sensor.read_sealevel_pressure()))
    #print()

if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(8000)
    # Generate some requests.
    while True:
        do_work()
