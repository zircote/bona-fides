# coding: utf-8
#
# Copyright [2015] [Robert Allen]
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
import os
from setuptools import setup

setup(
    name='bona-fides',
    version='0.0.3',
    long_description=__doc__,
    packages=['bona_fides'],
    include_package_data=True,
    zip_safe=False,
    install_requires=['httplib2',
                      'M2Crypto',
                      'nose'
    ]
)