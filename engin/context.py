# -*- coding: utf-8 -*-
from typing import Optional
import coppyr


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


context = Context()
