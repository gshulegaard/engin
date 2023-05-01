import copy

from coppyr import logger as clogger


def setup(log_path):
    config = copy.deepcopy(clogger.DEFAULT_CONFIG)
    config["handlers"]["file-default"]["filename"] = log_path

    clogger.setup(dict_config=config)


def get(name, level=None):
    return clogger.get(name=name, level=level)
