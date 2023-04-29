# -*- coding: utf-8 -*-
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

import crossplane
from crossplane.builder import build_files


@dataclass
class CrossplaneParsePayload:
    status: str = "ok"
    errors: List[Any] = field(default_factory=list)
    config: List[Any] = field(default_factory=list)

    def to_dict(self):
        return {
            "status": self.status,
            "errors": self.errors,
            "config": self.config
        }


def load(file_path: str) -> CrossplaneParsePayload:
    return CrossplaneParsePayload(
        **crossplane.parse(file_path)
    )


def dumps(
    payload: CrossplaneParsePayload
) -> List[str]:
    return [
        crossplane.build(cfg["parsed"], indent=2) for cfg in payload.config
    ]


def dump(
    payload: CrossplaneParsePayload,
    directory: Optional[str]=None
) -> None:
    build_files(payload.to_dict(), dirname=directory, indent=2)
