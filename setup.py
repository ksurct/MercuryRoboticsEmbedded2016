#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='ksurobot',
    version='0.1.0',
    packages=find_packages(exclude=['tasks']),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'ksurobot = ksurobot.main:main'
        ]
    },
    package_data = {
        'ksurobot': [
            'install/files/*',
        ]
    }
)
