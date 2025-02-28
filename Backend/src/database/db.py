import psycopg2
from psycopg2.pool import SimpleConnectionPool
from contextlib import contextmanager
import logging
from typing import Dict,Any
from datetime import datetime
from flask import current_app,g


logger = logging.getLogger(__name__)
app = current_app.get_current_object()

class DatabasePool:
    _pool = None

    @classmethod
    def initialize(cls):
        """
        Initialize the connection pool
        """
        if cls._pool is None:
            cls._pool = SimpleConnectionPool(
                minconn = 1,
                maxconn = 10,
                cursor_factory = RealDictCursor,
                host=app.config['DB_HOST'],
                port=app.config['DB_PORT'],
                user=app.config['DB_USER'],
                password=app.config['DB_PASSWORD'],
                database=app.config['DB_NAME']
            )
            logger.info("Database pool initialized")


    @classmethod
    def get_connection(cls):
        """Get a connection from the pool."""
        if cls._pool is None:
            raise Exception("Database pool is not initialized")
        return cls._pool.getconn()

    @classmethod
    def release_connection(cls, conn):
        """Release a connection back to the pool."""
        if cls._pool and conn:
            cls._pool.putconn(conn)

    @classmethod
    def close_all(cls):
        """Close all connections in the pool."""
        if cls._pool:
            cls._pool.closeall()