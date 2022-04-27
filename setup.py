"""
Python package configuration for scripts.

Thomas Dokas <dokastho@umich.edu>
"""

from setuptools import find_packages, setup

setup(
    name='snprocess',
    version='0.1.2',
    packages=find_packages(include=['snprocess', 'qc', 'templates'], exclude=['testout']),
    include_package_data=True,
    install_requires=[
        'pycodestyle',
        'pydocstyle',
        'pylint',
        'pytest',
        'pytest-mock',
        'click',
        'matplotlib',
        'pandas',
        'jinja2',
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'snprocess = snprocess.__main__:main'
        ]
    },
)
