from ddtrace import patch_all, tracer  # noqa
patch(flask=True)
patch_all()  # noqa
import signal
import os
import atexit
import time
import logging
import threading
from ddtrace import tracer
from datadog import statsd, initialize
from flask import Flask
import requests
tracer.configure(uds_path="/var/run/datadog/apm.socket")
tracer.set_tags({"env": os.environ.get("ENV")})
initialize(statsd_socket_path="/var/run/datadog/dsd.socket")

application = Flask(__name__)


@application.route("/")
def hello():
    logging.info("root get")
    return "<h1 style='color:blue'>Hello There!</h1>"


stopPrint = False


def doStop():
    logging.info("stop!")
    stopPrint = True


atexit.register(doStop)


def dogstatsd_test():
    logging.info("starting dogstatsd test")
    while not stopPrint:
        logging.info("incr!")
        statsd.increment("thread_function", 1.0, ["func:dogstatsd_test"])
        time.sleep(1)


def apm_test():
    logging.info("starting apm every 5 minutes")
    while not stopPrint:
        time.sleep(5)
        r = requests.get('http://localhost:5000')
        logging.info("Status code %d", r.status_code)


if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")
    logging.info("thread start")
    threading.Thread(target=dogstatsd_test).start()
    logging.info("app run")
    if os.environ["DATADOG_SERVICE_NAME"] == "ddclient":
        apm_test()
    else:
        application.run(host='0.0.0.0')
