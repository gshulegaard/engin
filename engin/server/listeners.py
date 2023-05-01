# -*- coding: utf-8 -*-
# https://sanic.dev/en/guide/basics/listeners.html#order-of-execution
# https://github.com/sanic-org/sanic/issues/2139#issuecomment-868993668


async def start_supervisor(app):
    """
    We use a listener here so we can insert a single background task that will
    run on the main sanic process.
    """
    from engin.server.tasks import supervisor
    app.add_task(supervisor.run(app))
