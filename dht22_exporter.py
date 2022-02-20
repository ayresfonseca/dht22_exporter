import time
import board
import adafruit_dht
from prometheus_client import start_http_server, Gauge

dht22_temperature_celsius = Gauge(
    "dht22_temperature_celsius",
    "Temperature in celsius provided by dht sensor",
    ["sensor"],
)
dht22_humidity = Gauge(
    "dht22_humidity", "Humidity in percents provided by dht sensor", ["sensor"]
)


def read_sensor(sensor, label):
    try:
        temperature = sensor.temperature
        humidity = sensor.humidity
        dht22_humidity.labels(label).set("{:.1f}".format(humidity))
        dht22_temperature_celsius.labels(label).set("{:.1f}".format(temperature))
    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        print(error.args[0])


if __name__ == "__main__":
    # Start up the server to expose the metrics.
    start_http_server(9101)
    dhtDevice1 = adafruit_dht.DHT22(board.D4, use_pulseio=False)
    dhtDevice2 = adafruit_dht.DHT22(board.D22, use_pulseio=False)

    while True:
        read_sensor(dhtDevice1, "sensor1")
        read_sensor(dhtDevice2, "sensor2")
        time.sleep(2.0)
