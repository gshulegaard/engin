# -*- coding: utf-8 -*-
from dataclasses import dataclass, field
from typing import Any, List, Optional

import crossplane
from crossplane.builder import build_files


from engin.nginx.objects import CrossplaneParsePayload, NginxConfig


def load(file_path: str) -> CrossplaneParsePayload:
    return CrossplaneParsePayload(
        **crossplane.parse(file_path)
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
