# -*- coding: utf-8 -*-
import os

from tempfile import TemporaryDirectory

from tests import here, BaseTestCase

from engin.nginx import config, toml


class NGINXConfigTestCase(BaseTestCase):
    config_root = os.path.join(here, "fixtures", "nginx", "configs")

    def test_simple_parse(self):
        """
        Just exercise the parse function on a valid NGINX config.
        """
        config_path = os.path.join(self.config_root, "simple", "nginx.toml")
        parsed = toml.load(config_path)
        assert isinstance(parsed, config.CrossplaneParsePayload)
        assert parsed.status == "ok"
        assert parsed.errors == []
        assert len(parsed.config) == 1
        assert parsed.config[0].errors == []

        import pprint
        print(pprint.pprint(parsed.config[0].to_dict(), indent=2))

        assert parsed.config[0].to_dict() == {
            "errors": [],
            "file": "nginx.conf",
            "parsed": [
                {
                    'args': [],
                    'block': [
                        {
                            'args': ['1024'],
                            'directive': 'worker_connections'
                        }
                    ],
                    'directive': 'events'
                },
                {
                    'args': [],
                    'block': [
                        {
                            'args': [],
                            'block': [
                                {
                                    'args': ['127.0.0.1:8080'],
                                    'directive': 'listen'
                                },
                                {
                                    'args': ['default_server'],
                                    'directive': 'server_name'
                                },
                                {
                                    'args': ['/'],
                                    'block': [
                                        {
                                            'args': ['200', 'foo bar baz'],
                                            'directive': 'return'
                                        }
                                    ],
                                    'directive': 'location'
                                }
                            ],
                            'directive': 'server'
                        }
                    ],
                    'directive': 'http'
                }
            ]
        }

