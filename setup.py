#! /usr/bin/env python3
# -*- coding: utf-8 -*-
from setuptools import find_packages, setup

from coppyr import package as pkg

from engin import (__title__, __summary__, __url__, __version__, __author__,
                   __email__, __license__)


setup(
    name=__title__,
    version=__version__,
    description=__summary__,
    long_description=pkg.get_readme("README.md"),
    long_description_content_type="text/markdown; charset=UTF-8",
    author=__author__,
    author_email=__email__,
    url=__url__,
    packages=find_packages(exclude=["tests", "tests.*"]),
    license=__license__,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    cmdclass={"upload": pkg.UploadCommand},
    install_requires=pkg.parse_requirements("/opt/engin/requirements.txt"),
    extras_require=pkg.parse_extras(
        dev="/opt/engin/requirements-dev.txt"
    ),
    include_package_data=True  # Read MANIFEST.in
)
