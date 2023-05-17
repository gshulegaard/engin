# -*- coding: utf-8 -*-
import signal
import time

from engin.context import context


def run():
    run = True

    # Signal handling
    # https://github.com/sanic-org/sanic/pull/2499
    def stop(*_):
        nonlocal run
        run = False

    signal.signal(signal.SIGINT, stop)
    signal.signal(signal.SIGTERM, stop)

    context.log.info("hello from run of sup")
    while run:
        context.log.info("Hello from supervisor!")
        time.sleep(5)
