import Adafruit_DHT
import datetime
from prometheus_client import start_http_server, Summary, Gauge

DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4
hum_metric = Gauge('humidity', 'Current humidity')
temp_metric = Gauge('temperature', 'Current temperature')

def do_work():
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    if humidity == None:
       print("cannot read humidity")
       return
    if humidity > 100:
       print("Abnormal value for humidity")
       return
    hum_metric.set(humidity)
    temp_metric.set(temperature)
    print("Date = {0}, Temp = {1:0.1f}*C, Humidity = {2:0.1f}%".format(datetime.datetime.now(), temperature, humidity))

if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(8000)
    # Generate some requests.
    while True:
        do_work()
