import psycopg2
from psycopg2.pool import SimpleConnectionPool
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager
import logging
from typing import Dict,Any
from datetime import datetime


logger = logging.getLogger(__name__)

class DatabasePool:
    _pool = None

    @classmethod
    def initialize()