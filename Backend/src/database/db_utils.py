from typing import Dict, List, Any, Optional
from flask import current_app, g
import logging


logger = logging.getLogger(__name__)

class DatabaseUtils:
    @staticmethod
    def editData(query: str,params: tuple = None)-> Optional[Dict]:
        try:
            g.db_cursor.execute(query,params)
            result = g.db_cursor.fetchone()
            return result
        except Exception as e:
            logger.error(f"Error executing query: {e}")
            raise

    @staticmethod
    def editDataInTransaction(queries: List[Dict[str,Any]])-> List[Dict]:
        results = []
        try:
            for query_dict in queries:
                g.db_cursor.execute(query_dict['query'], query_dict['params'])
                if g.db_cursor.description:  # If query returns something
                    result = g.db_cursor.fetchone()
                    results.append(result)
            return results
        except Exception as e:
            logger.error(f"Database error in editDataInTransaction: {str(e)}")
            
            
    @staticmethod
    def fetchData(query: str,params: tuple = None)-> List[Dict]:
        try:
            g.db_cursor.execute(query,params)
            result = g.db_cursor.fetchall()
            return result
        except Exception as e:
            logger.error(f"Error executing query: {e}")
            raise


    @staticmethod
    def fetchOne(query: str,params: tuple = None)-> Dict:
        try:
            g.db_cursor.execute(query,params)
            result = g.db_cursor.fetchone()
            return result
        except Exception as e:
            logger.error(f"Error executing query: {e}")
            raise