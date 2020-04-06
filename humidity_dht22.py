import Adafruit_DHT
import datetime
from prometheus_client import start_http_server, Summary, Gauge
import argparse

DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4

hum_metric = Gauge('humidity', 'Current humidity', ['room'])
temp_metric = Gauge('temperature', 'Current temperature', ['room'])

def do_work(room_name=None):
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    if humidity == None:
       print("cannot read humidity")
       return
    if humidity > 100:
       print("Abnormal value for humidity")
       return
    hum_metric.labels(room=room_name).set(humidity)
    temp_metric.labels(room=room_name).set(temperature)
    print("Date = {0}, Temp = {1:0.1f}*C, Humidity = {2:0.1f}%".format(datetime.datetime.now(), temperature, humidity))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=8000, help="Port to export the metrics on.")
    parser.add_argument('--room_name', required=True, type=str, help='Room name to export in metrics.')
    args = parser.parse_args()
    # Start up the server to expose the metrics.
    start_http_server(args.port)
    # Generate some requests.
    while True:
        do_work(args.room_name)
