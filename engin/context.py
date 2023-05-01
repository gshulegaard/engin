# -*- coding: utf-8 -*-
from typing import Optional
import coppyr
from coppyr.types import lazyproperty


class Context(coppyr.Context):
    def __init__(
        self,
        app_name: Optional[str]=None,
        config_path: Optional[str]=None,
        reinitialize: bool=False
    ):
        app_name = app_name if app_name is not None else "engin"
        super().__init__(
            app_name=app_name,
            config_path=config_path,
            reinitialize=reinitialize
        )

    @lazyproperty
    def log(self):
        from engin import logger

        log_path = self.config.get("LOG_PATH", f"/tmp/{self.app_name}.log")
        logger.setup(
            log_path
        )

        return logger.get(
            self.config.get("LOG_HANDLER", "file"), level=self.config.LOG_LEVEL
        )


context = Context(app_name="engin")
