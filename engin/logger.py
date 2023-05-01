import copy

from coppyr import logger as clogger


def get_default_config(log_path):
    config = copy.deepcopy(clogger.DEFAULT_CONFIG)
    config["handlers"]["file-default"]["filename"] = log_path
    return config


def setup(log_path):
    clogger.setup(dict_config=get_default_config(log_path))


def get(name, level=None):
    return clogger.get(name=name, level=level)
