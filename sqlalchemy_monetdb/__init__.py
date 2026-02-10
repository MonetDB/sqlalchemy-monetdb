"""
SQLAlchemy backend for MonetDB
"""

__version__ = '2.1.0a0'

import sqlalchemy

modern_sqlalchemy = not sqlalchemy.__version__.startswith('1')
