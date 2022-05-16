# piaware-exporter
Prometheus metrics exporter for PiAware

Exposes PiAware status information in the form of Prometheus metrics to port 9101. It polls piaware status.json for the status info.

## Usage
piaware-exporter takes in several input args to specify where to read piaware status.json, what port to expose Prometheus metrics to, and the interval to fetch piaware status.

```
python3 main.py -h

usage: main.py [-h] [--piaware_host PIAWARE_HOST] [--piaware_port PIAWARE_PORT] [--expo_port EXPO_PORT]
               [--fetch_interval FETCH_INTERVAL]

optional arguments:
  -h, --help            show this help message and exit
  --piaware_host PIAWARE_HOST
                        Host IP address to connect to for piaware status JSON
  --piaware_port PIAWARE_PORT
                        Host port to connect to for piaware status JSON
  --expo_port EXPO_PORT
                        Local port to export PiAware metrics on
  --fetch_interval FETCH_INTERVAL
                        Interval to read piaware status
```

### Example Usage
```
python3 main.py --piaware_host 192.168.0.200 --piaware_port 8080 --expo_port 9101 --fetch_interval 15
```
