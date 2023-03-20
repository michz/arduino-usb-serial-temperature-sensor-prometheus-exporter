"""Application exporter"""

import math
import os
import serial

from prometheus_client import start_http_server, CollectorRegistry, Gauge

class MetricsExporter:
    """
    Representation of Prometheus metrics and loop to fetch and transform
    application metrics into Prometheus metrics.
    """

    def __init__(self):
        self._temperature = math.nan
        self._humidity = math.nan
        self._registry = CollectorRegistry()

        # Prometheus metrics to collect
        self.metric_temperature = Gauge("environment_temperature", "Temperature in degree celsius", registry=self._registry)
        self.metric_humidity = Gauge("environment_humidity", "Relative Humidity in percent", registry=self._registry)

    def set_values(self, temperature, humidity):
        """
        Set the metrics to the given values
        """
        self.metric_temperature.set(temperature)
        self.metric_humidity.set(humidity)

    def run_server(self, port):
        """
        Runs the HTTP server in the background
        """
        start_http_server(exporter_port, registry=self._registry)

if __name__ == "__main__":
    exporter_port = int(os.getenv("EXPORTER_PORT", 9201))
    sensor_file = os.getenv("SENSOR_FILE", "/dev/ttyUSB0")
    baud_rate = int(os.getenv("BAUD_RATE", "115200"))

    print(f"Exporter port: {exporter_port}")
    print(f"Sensor file:   {sensor_file}")
    print(f"Baud rate:     {baud_rate}")

    metrics_exporter = MetricsExporter()
    metrics_exporter.run_server(baud_rate)

    #with open(sensor_file, "rb") as f:
    with serial.Serial(port=sensor_file, baudrate=baud_rate) as f:
        for line in f:
            temperature, humidity = line.rstrip().split(b';' , 1)
            metrics_exporter.set_values(float(temperature), float(humidity))
