# -*- coding: utf-8 -*-
import unittest

from coppyr import Context
from coppyr import logger


# init context
context = Context(app_name="engin-testing")


# setup logging
logger.setup()
log = logger.get(level="DEBUG")


class BaseTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.setup_class()

    @classmethod
    def tearDownClass(cls):
        cls.teardown_class()
        super().tearDownClass()

    @classmethod
    def setup_class(cls):
        pass

    @classmethod
    def teardown_class(cls):
        pass

    def setup_method(self, method):
        context.inc_action_id()
        hdr = '=' * 20
        log.info(
            f'{hdr} {self.__class__.__name__} {self._testMethodName} {hdr}'
        )

    def teardown_method(self, method):
        pass
