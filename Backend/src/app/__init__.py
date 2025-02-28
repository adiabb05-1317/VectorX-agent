from flask import Flask, g ,request 
import time
import logging
from src.config import Config
from psycopg2.extras import RealDictCursor
from src.database.db import DatabasePool



def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)


    #just logging configuration
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    

    #initialize the database
    DatabasePool.initialize()

    @app.before_request
    def before_request():

        #Store request start time   
        g.start_time = time.time()


        #get a connection from the pool
        g.db_conn = DatabasePool.get_connection()
        g.db_cursor = g.db_conn.cursor(cursor_factory=RealDictCursor)  


        g.user_id = None # this will be set by auth middleware->ongo

        app.logger.info(f"Request started at {g.start_time}")


    @app.after_request
    def after_request(response):
        #Calculate request duration
        duration = time.time() - g.start_time

        app.logger.info(f"Request ended at {time.time()} and took {duration} seconds" f" status code {response.status_code}")
        if hasattr(g, 'db_conn'):
            try:
                g.db_conn.commit()
            except Exception as e:
                g.db_conn.rollback()
                logging.error(f"Transaction rolled back due to: {e}")
            finally:
                DatabasePool.release_connection(g.db_conn) #release or put back in pool        



        return response
    
    @app.teardown_appcontext
    def teardown_db(exception):
        
        if hasattr(g,'db_conn'):
            DatabasePool.release_connection(g.db_conn)

    #register blueprint here
    from src.app.routes import main_bp
    app.register_blueprint(main_bp)    



    return app