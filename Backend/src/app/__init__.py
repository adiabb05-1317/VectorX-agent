from flask import Flask, g ,request 
import time
import logging
from src.config import Config
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

        g.user_id = None # this will be set by auth middleware->ongo

        app.logger.info(f"Request started at {g.start_time}")


    @app.after_request
    def after_request(response):
        #Calculate request duration
        duration = time.time() - g.start_time

        app.logger.info(f"Request ended at {time.time()} and took {duration} seconds" f" status code {response.status_code}")

        return response
    
    @app.teardown_appcontext
    def teardown_db(exception):
        DatabasePool.close_all()

    #register blueprint here
    from src.app.routes import main_bp
    app.register_blueprint(main_bp)    



    return app