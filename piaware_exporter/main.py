#!/usr/bin/python3

import argparse
from prometheus_client import start_http_server
import signal
import sys

from exporter import PiAwareMetricsExporter

def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--piaware_host",
        help="Host IP address to connect to for piaware status JSON",
        default="localhost"
        )

    parser.add_argument(
        "--piaware_port",
        help="Host Port to connect to for piaware status JSON",
        default="8080"
        )

    parser.add_argument(
        "--expo_port",
        help="Local port to export PiAware metrics on",
        default="9101", type=int
        )

    args = parser.parse_args()

    return args

def signal_handler(signal, frame):
    print ('piaware_exporter shutting down.')
    sys.exit(0)

def main():
    print('PiAware Prometheus Exporter starting.')
    # Get program args
    args = getArgs()

    # Create PiAwareMetrics object that reads and exports status information
    piaware_exporter = PiAwareMetricsExporter(args.piaware_host, args.piaware_port)

    # Bring up endpoint to expose the Prometheus metrics on
    start_http_server(args.expo_port)

    # Set up signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Start fetching
    piaware_exporter.start_fetch_loop()

if __name__ == "__main__":
    main()
