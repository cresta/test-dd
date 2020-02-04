from ddtrace import patch_all, tracer # noqa
patch_all() # noqa
import signal
import atexit
import time
import logging
import threading
from ddtrace import tracer
from datadog import statsd, initialize
from flask import Flask
tracer.configure(uds_path="/var/run/datadog/dsd.socket")
initialize({"statsd_socket_path": "/var/run/datadog/dsd.socket"})

application = Flask(__name__)


@application.route("/")
def hello():
    return "<h1 style='color:blue'>Hello There!</h1>"


stopPrint = False


def doStop():
    logging.info("stop!")
    stopPrint = True


atexit.register(doStop)


def thread_function():
    logging.info("starting!")
    while not stopPrint:
        logging.info("incr!")
        statsd.increment("thread_function", 1.0, {"func": "thread_function"})
        time.sleep(1)


if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")
    logging.info("thread start")
    threading.Thread(target=thread_function).start()
    logging.info("app run")
    application.run(host='0.0.0.0')
