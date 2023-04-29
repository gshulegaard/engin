# -*- coding: utf-8 -*-
from dataclasses import dataclass, field
from typing import List, Optional

from engin.nginx.objects.abstract import AbstractNginxObject


@dataclass
class NginxDirective(AbstractNginxObject):
    directive: str
    args: List[str] = field(default_factory=list)
    block: Optional[List[AbstractNginxObject]] = None
    includes: Optional[List[int]] = None
    line: Optional[int] = None

    # TODO: Figure out best way to nest a type in a dataclass (self.block).

    def __post_init__(self):
        if self.block is not None:
            self.block = [
                NginxDirective(**i) if isinstance(i, dict) else i
                for i in self.block
            ]

    def to_dict(self):
        result = {
            "directive": self.directive,
            "args": self.args
        }

        # Only include optional values if they were specified
        for field in ("includes", "line"):
            value = getattr(self, field)
            if value is not None:
                result[field] = value

        # Walk the block tree and call to_dict() for nested directives
        if self.block is not None:
            result["block"] = [i.to_dict() for i in self.block]

        return result
