# -*- coding: utf-8 -*-
from dataclasses import dataclass, field
from typing import Any, List, Optional

from engin.nginx.objects.abstract import AbstractNginxObject
from engin.nginx.objects.directive import NginxDirective


@dataclass
class NginxConfig(AbstractNginxObject):
    file: str
    status: Optional[str] = None
    errors: List[Any] = field(default_factory=list)
    parsed: List[NginxDirective] = field(default_factory=list)

    def __post_init__(self):
        self.parsed = [
            NginxDirective(**i) if isinstance(i, dict) else i
            for i in self.parsed
        ]

    def to_dict(self):
        result = {
            "file": self.file,
            "errors": self.errors,
            "parsed": [i.to_dict() for i in self.parsed]
        }

        if self.status is not None:
            result["status"] = self.status

        return result
