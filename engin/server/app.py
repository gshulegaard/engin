# -*- coding: utf-8 -*-
from sanic import Sanic

from engin import __version__
from engin.context import context


context.app_name = "engin-api"


app = Sanic(
    context.app_name,
    ctx=context
)
# Apply Sanic configuration values from engin config
app.config.update(**context.config.get("server", {}))


## Update openapi meta
from textwrap import dedent
app.ext.openapi.describe(
    "engin API",
    version=__version__,
    description=dedent(
        """
        engin (Easy-NGINX) is an NGINX sidecar utility that provides an API and
        tries to simplify server administration.
        """
    ),
)


## Add listeners
if context.environment != "testing":  # skip in testing
    from engin.server import listeners
    app.register_listener(listeners.start_supervisor, "after_server_start")
    # This will register a supervisor on every worker after they are started.

## Add routes
from engin.server.views.health import Health
app.add_route(Health.as_view(), "/health")
