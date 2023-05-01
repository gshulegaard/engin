# -*- coding: utf-8 -*-
import sanic
from sanic.response import text, HTTPResponse
from sanic.views import HTTPMethodView
from sanic_ext import openapi


class Health(HTTPMethodView):
    @openapi.definition(
        summary="Health check endpoint",
        response=[openapi.definitions.Response(text("Pong!"))]
    )
    async def get(self, request: sanic.Request):
        app = sanic.Sanic.get_app()
        app.ctx.log.info("Hello from get health new")
        return text("Pong!")
