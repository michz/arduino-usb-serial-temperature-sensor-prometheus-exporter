# Prometheus Exporter for arduino-usb-serial-temperature-sensor

Collects the sensor measurements and exposes them as a Prometheus Exporter via HTTP.

It uses a custom `CollectorRegistry` to avoid exporting the default python metrics,
which are not relevant in this use case at all and would bloat the TSDB unnecessarily much.

It expects data on the serial port in the form of:

```
temp;hum\n
23.45;55.55\n
```

## Build

```
docker build -t prometheus-exporter-arduino-usb-serial-temperature-sensor .
```

## Run

```
docker run \
    --device /dev/ttyUSB0 \
    -p 9201 \
    prometheus-exporter-arduino-usb-serial-temperature-sensor
```

## Environment variables (configuration)

```
Variable            Default
--------            -------
EXPORTER_PORT       9201
SENSOR_FILE         /dev/ttyUSB0
BAUD_RATE           115200
```

## Debug with virtual serial port

```
# In one terminal:
sudo socat -dd pty,raw,echo=0,link=/tmp/ttyTestIn pty,raw,echo=0,link=/tmp/ttyTestOut

# In another terminal:
docker run \
    -v /tmp/ttyTestOut:/dev/ttyUSB0 \
    -p 9201 \
    prometheus-exporter-arduino-usb-serial-temperature-sensor

# In yet another terminal:
echo "12.45;55.55" | sudo tee /tmp/ttyTestIn

curl http://localhost:9201/
```

## License

MIT
