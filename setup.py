# coding: utf-8
import os
from setuptools import setup

setup(
    name='bona-fides',
    version='0.0.1',
    long_description=__doc__,
    packages=['bona_fides'],
    include_package_data=True,
    zip_safe=False,
    install_requires=['httplib2',
                      'M2Crypto',
                      'nose'
    ]
)