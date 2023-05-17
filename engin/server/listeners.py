# -*- coding: utf-8 -*-
# https://sanic.dev/en/guide/basics/listeners.html#order-of-execution
# https://github.com/sanic-org/sanic/issues/2139#issuecomment-868993668a
from sanic import Sanic

from engin.server.app import app


@app.main_process_ready
async def start_supervisor(app: Sanic):
    """
    We use a listener as a convenient way for starting a supervisor process.

    See this blog about running managed processes:
      - https://amhopkins.com/background-job-worker

    Also this issue from sanic:
      - https://github.com/sanic-org/sanic/pull/2499
    """
    from engin.server.tasks import supervisor
    app.manager.manage(
        "EnginSupervisor", supervisor.run, {}
    )
