"""
Python package configuration for scripts.

Thomas Dokas <dokastho@umich.edu>
"""

from setuptools import setup

setup(
    name='qc',
    version='0.1.0',
    packages=['qc'],
    include_package_data=True,
    install_requires=[
        'pycodestyle',
        'pydocstyle',
        'pylint',
        'pytest',
        'pytest-mock',
        'pandas_plink',
    ],
    python_requires='>=3.6',
)
