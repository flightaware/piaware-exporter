
from prometheus_client import Enum, Counter, Gauge
import requests
import time

class PiAwareMetricsExporter():
    ''' Fetches status from PiAware, generates Prometheus metrics with that data, and 
        exports them to an endpoint.
    '''
    def __init__(self, host, port, fetch_interval=15):
        self.piaware_status_url = f"http://{host}:{port}"
        self.fetch_interval = fetch_interval

        # Prometheus metrics to collect and expose
        self.radio_state = Enum('piaware_radio_state', 'Radio Status', states=['green', 'amber', 'red', 'N/A'])
        self.piaware_state = Enum('piaware_service_state', 'PiAware Service Status', states=['green', 'amber', 'red', 'N/A'])
        self.flightaware_connection_state = Enum('piaware_connect_to_flightaware_state', 'FlightAware Connection Status', states=['green', 'amber', 'red', 'N/A'])
        self.mlat_state = Enum('piaware_mlat_state', 'MLAT Status', states=['green', 'amber', 'red', 'N/A'])

    def start_fetch_loop(self):
        ''' Main loop to do periodic fetches of piaware status.json

        '''
        while True:
            self.fetch_piaware_status()
            time.sleep(self.fetch_interval)

    def fetch_piaware_status(self):
        ''' Fetch piaware status.json and update Prometheus metric

        '''
        try:
            response = requests.get(url=f'{self.piaware_status_url}/status.json')
        except requests.exceptions.ConnectionError:
            print (f"Could not connect to {self.piaware_status_url}")
            return
        except requests.exceptions.Timeout:
            print (f"Timeout Error requesting {self.piaware_status_url}")
            return
        except Exception as e:
            print(f"Error reading piaware status.json: {e}")
            return

        if response.status_code != 200:
            # Error reading piaware status.json
            self.piaware_state.state("N/A")
            self.flightaware_connection_state.state("N/A")
            self.mlat_state.state("N/A")
            self.radio_state.state("N/A")
            return
        
        request_json = response.json()

        piaware = request_json.get("piaware")
        flightaware_connection = request_json.get("adept")
        mlat = request_json.get("mlat")
        radio = request_json.get("radio")

        if piaware:
            status = piaware.get("status")
            if status == "green":
                self.piaware_state.state("green")
            elif status == "amber":
                self.piaware_state.state("amber")
            else:
                self.piaware_state.state("red")


        if flightaware_connection:
            status = flightaware_connection.get("status")
            if status == "green":
                self.flightaware_connection_state.state("green")
            elif status == "amber":
                self.flightaware_connection_state.state("amber")
            else:
                self.flightaware_connection_state.state("red")


        if mlat:
            status = mlat.get("status")
            if status == "green":
                self.mlat_state.state("green")
            elif status == "amber":
                self.mlat_state.state("amber")
            else:
                self.mlat_state.state("red")


        if radio:
            status = radio.get("status")
            if status == "green":
                self.radio_state.state("green")
            elif status == "amber":
                self.radio_state.state("amber")
            else:
                self.radio_state.state("red")