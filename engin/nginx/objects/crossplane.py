from dataclasses import dataclass, field
from typing import Any, List

from engin.nginx.objects.config import NginxConfig


@dataclass
class CrossplaneParsePayload:
    status: str = "ok"
    errors: List[Any] = field(default_factory=list)
    config: List[NginxConfig] = field(default_factory=list)

    def __post_init__(self):
        self.config = [
            NginxConfig(**i) if isinstance(i, dict) else i
            for i in self.config
        ]

    def to_dict(self):
        return {
            "status": self.status,
            "errors": self.errors,
            "config": [conf.to_dict() for conf in self.config]
        }
