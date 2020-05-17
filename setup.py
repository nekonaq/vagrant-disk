#!/usr/bin/env python3
from setuptools import setup, find_packages
import re
import os

version = re.search("__version__ = '([^']+)'", open(
    os.path.join(os.path.dirname(__file__), 'vagrant_disk/__init__.py')
).read().strip()).group(1)

setup(
    name='vagrant-disk',
    version=version,
    description="Vagrant box file disk image extractor",
    author="Tatsuo Nakajyo",
    author_email="tnak@nekonaq.com",
    license='BSD',
    packages=find_packages(),
    python_requires='~=3.6.9',
    entry_points={
        'console_scripts': [
            'vagrant-disk = vagrant_disk.cli:Command.main',
        ]
    },
)

# compile-command: "python3 ./setup.py sdist"
# End:
