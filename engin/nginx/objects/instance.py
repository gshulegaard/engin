from dataclasses import dataclass, field
from enum import Enum
from typing import Any, List, Optional

from coppyr.process import subp

from engin.nginx import config as ngxcfg
from engin.nginx.objects.crossplane import CrossplaneParsePayload


# https://docs.nginx.com/nginx/admin-guide/basic-functionality/runtime-control/
class NginxSignal(Enum):
    QUIT   = "quit"    # SIGQUIT
    RELOAD = "reload"  # SIGHUP
    REOPEN = "reopen"  # SIGUSR1
    STOP   = "stop"    # SIGTERM


@dataclass
class NginxInstance:
    pid: int
    version: str
    bin_path: str
    conf_path: str
    prefix: str
    local_id: str
    workers: List[Any] = field(default_factory=list)
    config: Optional[CrossplaneParsePayload] = None

    def __post_init__(self):
        self.config = ngxcfg.load(self.conf_path)

    def signal(self, sig: NginxSignal) -> bool:
        status, _, _ = subp.call(f"{self.bin_path} -s {sig.value}", check=False)
        return True if status == 0 else False

    def reload(self) -> bool:
        return self.signal(NginxSignal.RELOAD)

    def test(self) -> bool:
        status, _, _ = subp.call(f"{self.bin_path} -t", check=False)
        return True if status == 0 else False
