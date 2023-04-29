# -*- coding: utf-8 -*-
import os
from tempfile import TemporaryDirectory

from tests import here, BaseTestCase

from engin.nginx import config
from engin.nginx.objects import NginxConfig


class NGINXConfigObjectTestCase(BaseTestCase):
    config_root = os.path.join(here, "fixtures", "nginx", "configs")

    def test_parse(self):
        config_path = os.path.join(self.config_root, "simple", "nginx.conf")
        config_obj = config.load(config_path).config[0]
        assert isinstance(config_obj, NginxConfig)

        # parse the same file
        config_obj_2 = config.load(config_path).config[0]
        assert config_obj == config_obj_2

    def test_equality_after_write(self):
        config_path = os.path.join(self.config_root, "simple", "nginx.conf")
        parsed = config.load(config_path)

        with TemporaryDirectory() as tmpdir:
            # change the file value to be in the tmpdir (otherwise dump would
            # just write over the existing file)
            parsed.config[0].file = os.path.join(tmpdir, "nginx.conf")

            config.dump(parsed)
            new_parsed = config.load(os.path.join(tmpdir, "nginx.conf"))

            # do a second write and parse to test equality
            parsed.config[0].file = os.path.join(tmpdir, "nginx.conf")

            config.dump(parsed)
            new_new_parsed = config.load(os.path.join(tmpdir, "nginx.conf"))


        config_obj = parsed.config[0]
        config_obj_2 = new_parsed.config[0]
        assert config_obj != config_obj_2
        # Because crossplane does not respect whitespace, the line numbers are
        # different

        # ... but if we were to write it out again, then the re-parse of the
        # crossplane style should be equal
        config_obj_3 = new_new_parsed.config[0]
        assert config_obj_2 == config_obj_3
