# -*- coding: utf-8 -*-
from typing import List, Optional

import crossplane
from crossplane.builder import build_files


from engin.nginx.objects import CrossplaneParsePayload


def load(file_path: str) -> CrossplaneParsePayload:
    return CrossplaneParsePayload(
        **crossplane.parse(
            file_path,
            comments=False,
            check_args=True,
            check_ctx=True
        )
    )


def dumps(
    payload: CrossplaneParsePayload
) -> List[str]:
    return [
        crossplane.build(cfg.to_dict()["parsed"], indent=2) for cfg in payload.config
    ]


def dump(
    payload: CrossplaneParsePayload,
    directory: Optional[str]=None
) -> None:
    build_files(payload.to_dict(), dirname=directory, indent=2)
