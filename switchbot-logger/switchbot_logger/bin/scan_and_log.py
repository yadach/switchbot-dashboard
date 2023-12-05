#!/usr/bin/env python3

import argparse
import logging
import time
from datetime import datetime
from datetime import timezone

import yaml
from bluepy import btle

from switchbot_logger.logger import DBHandler
from switchbot_logger.sensor import SwitchbotScanDelegate


def get_arguments():
    """Parse arguments."""
    parser = argparse.ArgumentParser(description="Description of the script.")
    parser.add_argument(
        "--conf",
        type=str,
        default="conf/default.yaml",
        help="Config file.",
    )
    parser.add_argument(
        "--mac",
        type=str,
        required=True,
        help="Switchbot MAC address.",
    )
    return parser.parse_args()


def scan_and_logging(
    db_conf: dict,
    mac: str,
) -> None:
    # get sensor data
    scanner = btle.Scanner().withDelegate(SwitchbotScanDelegate(mac))
    while True:
        scanner.scan(5.0)  # timeout 5.0sec
        if scanner.delegate.sensorValue is not None:
            break
        else:
            logging.warning("Scanning sensor data again...")
    logging.info(
        f"Temperature: {scanner.delegate.sensorValue['Temperature']}, "
        f"Humidity: {scanner.delegate.sensorValue['Humidity']}"
    )
    data = scanner.delegate.sensorValue
    data["Datetime"] = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

    # make data
    strs = [key for key in data.keys()]
    columns = ", ".join(strs)
    vals = "%(" + ")s, %(".join(strs) + ")"
    operation = f"INSERT INTO {db_conf['table']} ({columns}) VALUES({vals}s)"
    # insert data
    dbhandler = DBHandler(**db_conf)
    dbhandler.create_table(db_conf["table"])
    dbhandler.insert(operation, data)
    dbhandler.close()


if __name__ == "__main__":
    # set logger
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s (%(module)s:%(lineno)d) %(levelname)s: %(message)s",
    )

    args = get_arguments()
    conf_file = args.conf
    with open(conf_file) as file:
        conf = yaml.safe_load(file)
    conf["MAC"] = args.mac

    while True:
        scan_and_logging(db_conf=conf["DB"], mac=conf["MAC"])
        time.sleep(conf["Loop"]["sleep"])
