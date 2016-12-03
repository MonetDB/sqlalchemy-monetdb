#!/usr/bin/env python
"""
Setup for SQLAlchemy backend for MonetDB
"""
from setuptools import find_packages, setup
import os

readme = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

setup_params = dict(
    name="sqlalchemy_monetdb",
    version='0.9.2',
    description="SQLAlchemy dialect for MonetDB",
    author="Gijs Molenaar",
    author_email="gijsmolenaar@gmail.com",
    long_description=readme,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Database :: Front-Ends',
        ],
    keywords='MonetDB SQLAlchemy',
    packages=find_packages(),
    include_package_data=True,
    tests_require=['nose >= 0.11'],
    test_suite="run_tests.setup_py_test",
    zip_safe=False,
    entry_points={
        "sqlalchemy.dialects":
            ["monetdb = sqlalchemy_monetdb.dialect:MonetDialect"]
    },
    license="MIT",
    install_requires=['pymonetdb >= 0.1', 'sqlalchemy'],
)

if __name__ == '__main__':
    setup(**setup_params)
