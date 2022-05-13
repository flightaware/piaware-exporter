
'''
This script reads piaware status information obtained from piaware status.json
and exposes them to Prometheus for monitoring and visualization.
'''

#!/usr/bin/python3

import argparse
import logging
from prometheus_client import start_http_server
import signal
import sys
from exporter import PiAwareMetricsExporter

# Configure logging
logging.basicConfig(format='%(asctime)s - %(module)s - %(message)s', datefmt='%b %d %Y %H:%M:%S', level=logging.INFO)
logger = logging.getLogger()

def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--piaware_host",
        help="Host IP address to connect to for piaware status JSON",
        default="localhost"
        )

    parser.add_argument(
        "--piaware_port",
        help="Host port to connect to for piaware status JSON",
        default="8080"
        )

    parser.add_argument(
        "--expo_port",
        help="Local port to export PiAware metrics on",
        default="9101",
        type=int
        )

    parser.add_argument(
        "--fetch_interval",
        help="Interval to read piaware status",
        default=15,
        type=int
    )

    args = parser.parse_args()

    return args

def signal_handler(signal, frame):
    logger.info('PiAware Prometheus Exporter shutting down.')
    sys.exit(0)

def main():
    logger.info('PiAware Prometheus Exporter starting.')
    # Get program args
    args = getArgs()


    # Create PiAwareMetrics object that reads and exports status information
    piaware_exporter = PiAwareMetricsExporter(args.piaware_host, args.piaware_port, args.fetch_interval)

    # Bring up endpoint to expose the Prometheus metrics on
    try:
        start_http_server(args.expo_port)
        logger.info(f'Started Prometheus server endpoint on port {args.expo_port}')
    except Exception as e:
        logger.error(f'Could not start Prometheus server endpoint on port {args.expo_port}: {e}')
        sys.exit(1)

    # Set up signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Start fetching
    piaware_exporter.start_fetch_loop()

if __name__ == "__main__":
    main()
