MonetDB dialect for SQLAlchemy
==============================

This is the MonetDB dialect driver for SQLAlchemy. It has support for Python from 3.3 onwards and even PyPy. It supports
SQLalchemy 1.0, 1.1, 1.2, 1.3 & 1.4.


Installation
------------

To install this dialect run::

    $ pip install sqlalchemy_monetdb

or from the source folder::

    $ pip install .


Usage
-----

To start using this dialect::

    from sqlalchemy import create_engine
    engine = create_engine('monetdb://monetdb:monetdb@localhost:50000/demo', echo=True)

Alternatively, you can also specify the driver::

    engine = create_engine('monetdb+pymonetdb://monetdb:monetdb@localhost:50000/demo', echo=True)

More info
---------

 * http://www.sqlalchemy.org/
 * http://www.monetdb.org/


Development
-----------

.. image:: https://travis-ci.org/gijzelaerr/sqlalchemy-monetdb.png?branch=master
  :target: https://travis-ci.org/gijzelaerr/sqlalchemy-monetdb


