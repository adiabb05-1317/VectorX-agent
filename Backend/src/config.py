from dotenv import load_dotenv
import os

load_dotenv()


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    DATABASE_URL = os.getenv('DATABASE_URL')
    DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')                       

    #session details
    SESSION_TYPE = 'filesystem'
    SESSION_PERMANENT = False
    SESSION_TIME=1800 #30min
    
