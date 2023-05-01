# -*- coding: utf-8 -*-
import asyncio


async def run(app):
    while True:
        app.ctx.log.info("Hello from supervisor!")
        await asyncio.sleep(5)
