# -*- coding: utf-8 -*-
from typing import Optional
from coppyr.context import BaseContext
from coppyr.types import lazyproperty, Singleton


class Context(BaseContext, Singleton):
    def __init__(
        self,
        app_name: Optional[str]=None,
        config_path: Optional[str]=None,
        reinitialize: bool=False
    ):
        self.app_name = app_name if app_name is not None else "engin"

        super().__init__(
            app_name=app_name,
            config_path=config_path,
            reinitialize=reinitialize
        )

    @property
    def environment(self):
        return self.config.get("ENVIRONMENT", "production")

    @lazyproperty
    def log_path(self):
        return self.config.get("LOG_PATH", f"/tmp/{self.app_name}.log")

    @lazyproperty
    def log(self):
        from engin import logger

        logger.setup(self.log_path)

        return logger.get(
            self.config.get("LOG_HANDLER", "file"), level=self.config.LOG_LEVEL
        )


context = Context()
