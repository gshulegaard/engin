# -*- coding: utf-8 -*-
import os

from coppyr.process import subp
from tests import here, BaseTestCase

from engin.nginx import proc
from engin.nginx.objects import NginxSignal


class NGINXProcTestCase(BaseTestCase):
    def setup_method(self, method):
        super().setup_method(method)
        subp.call(f"/usr/sbin/nginx")

    def teardown_method(self, method):
        subp.call(f"/usr/sbin/nginx -s quit", check=False)
        super().teardown_method(method)

    def test_find(self):
        nginxs = proc.find()
        assert len(nginxs) == 1

        nginx = nginxs[0]
        print(nginx.prefix, nginx.conf_path, nginx.local_id)
        assert nginx.bin_path == "/usr/sbin/nginx"
        assert nginx.prefix == "/usr/share/nginx"
        assert nginx.conf_path == "/etc/nginx/nginx.conf"
        assert nginx.local_id == \
            "151d8728e792f42e129337573a21bb30ab3065d59102f075efc2ded28e713ff8"

    def test_signals(self):
        nginx = proc.find()[0]
        assert nginx.signal(NginxSignal.RELOAD)
        assert nginx.reload()
        assert nginx.test()
