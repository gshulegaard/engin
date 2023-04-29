# -*- coding: utf-8 -*-
import os

from tempfile import TemporaryDirectory

from tests import here, BaseTestCase

from engin.nginx import config


class NGINXConfigTestCase(BaseTestCase):
    config_root = os.path.join(here, "fixtures", "nginx", "configs")

    def test_simple_parse(self):
        """
        Just exercise the parse function on a valid NGINX config.
        """
        config_path = os.path.join(self.config_root, "simple", "nginx.conf")
        parsed = config.load(config_path)
        assert isinstance(parsed, config.CrossplaneParsePayload)
        assert parsed.status == "ok"
        assert parsed.errors == []
        assert len(parsed.config) == 1
        assert parsed.config[0]["errors"] == []

        assert parsed.config[0] == {
            "status": "ok",
            "errors": [],
            "file": "/opt/engin/tests/fixtures/nginx/configs/simple/nginx.conf",
            "parsed": [
                {
                    'args': [],
                    'block': [
                        {
                            'args': ['1024'],
                            'directive': 'worker_connections',
                            'line': 2
                        }
                    ],
                    'directive': 'events',
                    'line': 1
                },
                {
                    'args': [],
                    'block': [
                        {
                            'args': [],
                            'block': [
                                {
                                    'args': ['127.0.0.1:8080'],
                                    'directive': 'listen',
                                    'line': 7
                                },
                                {
                                    'args': ['default_server'],
                                    'directive': 'server_name',
                                    'line': 8
                                },
                                {
                                    'args': ['/'],
                                    'block': [
                                        {
                                            'args': ['200', 'foo bar baz'],
                                            'directive': 'return',
                                            'line': 10
                                        }
                                    ],
                                    'directive': 'location',
                                    'line': 9
                                }
                            ],
                            'directive': 'server',
                            'line': 6
                        }
                    ],
                    'directive': 'http',
                    'line': 5
                }
            ]
        }

    def test_simple_dump(self):
        """
        Parse an NGINX config, dump it to a new file, and then re-parse the new
        file to ensure it is valid.

        NOTE: The contents of the new file will be different as crossplane
        strips whitespace.
        """
        config_path = os.path.join(self.config_root, "simple", "nginx.conf")
        parsed = config.load(config_path)

        with TemporaryDirectory() as tmpdir:
            # change the file value to be in the tmpdir (otherwise dump would
            # just write over the existing file)
            parsed.config[0]["file"] = os.path.join(tmpdir, "nginx.conf")

            config.dump(parsed)
            new_parsed = config.load(os.path.join(tmpdir, "nginx.conf"))

        assert isinstance(new_parsed, config.CrossplaneParsePayload)
        assert new_parsed.status == "ok"
        assert new_parsed.errors == []
        assert len(new_parsed.config) == 1
        assert new_parsed.config[0]["errors"] == []
        assert new_parsed.config[0]["file"] == os.path.join(tmpdir, "nginx.conf")

    def test_simple_dumps(self):
        config_path = os.path.join(self.config_root, "simple", "nginx.conf")
        parsed = config.load(config_path)

        dumps = config.dumps(parsed)
        assert len(dumps) == 1
        assert dumps == [
            'events {\n'
            '  worker_connections 1024;\n'
            '}\n'
            'http {\n'
            '  server {\n'
            '    listen 127.0.0.1:8080;\n'
            '    server_name default_server;\n'
            '    location / {\n'
            "      return 200 'foo bar baz';\n"
            '    }\n'
            '  }\n'
            '}'
        ]

