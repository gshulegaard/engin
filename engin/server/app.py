# -*- coding: utf-8 -*-
from sanic import Sanic

from engin import __version__
from engin.context import context


# https://sanic.dev/en/guide/deployment/manager.html#how-sanic-server-starts-processes
Sanic.start_method = "fork"


context.app_name = "engin-api"
context.config  # load config

app = Sanic(
    context.app_name,
    ctx=context
)

# Apply Sanic configuration values from engin config
app.config.update(
    **context.config.get("server", {})
)


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
    from engin.server.listeners import *

## Add routes
from engin.server.views.health import Health
app.add_route(Health.as_view(), "/health")
