#!/usr/bin/python3

from enum import Enum
import requests
import time
from prometheus_client import start_http_server, Enum, Counter, Gauge


class PiAwareMetricsExporter():
    ''' Fetches status from PiAware, generates Prometheus metrics with that data, and 
        exports them to an endpoint.
    '''
    def __init__(self, piaware_status_port=8080, fetch_interval=15):
        self.piaware_status_port = piaware_status_port
        self.fetch_interval = fetch_interval

        # Prometheus metrics to collect and expose
        self.radio_state = Enum('piaware_radio_state', 'Radio Status', states=['up', 'down'])
        self.piaware_state = Enum('piaware_service_state', 'PiAware Service Status', states=['up', 'down'])
        self.flightaware_connection_state = Enum('piaware_connect_to_flightaware_state', 'FlightAware Connection Status', states=['up', 'down'])
        self.mlat_state = Enum('piaware_mlat_state', 'MLAT Status', states=['up', 'down'])
        self.piaware_version = Gauge('piaware_version_info', 'PiAware Software Version', labelnames=['version'])

    def start_fetch_loop(self):
        ''' Main loop to do periodic fetches of piaware status.json

        '''
        while True:
            self.fetch_piaware_status()
            time.sleep(self.fetch_interval)

    def fetch_piaware_status(self):
        ''' Fetch piaware status.json and update Prometheus metric

        '''
        r = requests.get(url=f'http://localhost:{self.piaware_status_port}/status.json')
        
        request_json = r.json()


def main():

    # Create PiAwareMetrics object
    piaware_exporter = PiAwareMetricsExporter()

    # Bring up endpoint to expose the Prometheus metrics
    start_http_server(9101)

    # Start fetching
    piaware_exporter.start_fetch_loop()

if __name__ == "__main__":
    main()
