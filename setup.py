#!/usr/bin/env python
"""
Setup for SQLAlchemy backend for MonetDB
"""
from setuptools import find_packages, setup
import os

tests_require = ['pytest', 'coverage', 'mypy']

extras_require = {
    'monetdbe': ['monetdbe'],
    'test': tests_require
}

readme = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

setup_params = dict(
    name="sqlalchemy_monetdb",
    version='2.0.0',
    description="SQLAlchemy dialect for MonetDB",
    author="Gijs Molenaar",
    author_email="gijsmolenaar@gmail.com",
    url="https://github.com/gijzelaerr/sqlalchemy-monetdb",
    long_description=readme,
    extras_require=extras_require,
    classifiers=[
        "Topic :: Database",
        "Topic :: Database :: Database Engines/Servers",
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Database :: Front-Ends",
        ],
    keywords='MonetDB SQLAlchemy',
    packages=find_packages(),
    include_package_data=True,
    setup_requires=['pytest-runner', 'sqlalchemy'],
    tests_require=tests_require,
    test_suite="test.test_suite",
    zip_safe=False,
    entry_points={
        "sqlalchemy.dialects": [
            "monetdb = sqlalchemy_monetdb.dialect:MonetDialect",
            "monetdb.pymonetdb = sqlalchemy_monetdb.dialect:MonetDialect",
        ]
    },
    license="MIT",
    install_requires=['pymonetdb', 'sqlalchemy'],
)

if __name__ == '__main__':
    setup(**setup_params)
