import os
from dotenv import load_dotenv

# load .env into os.environ at import time
load_dotenv()

class Settings:
    
    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM = os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES:int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "10"))

    POSTGRES_URL = os.getenv("POSTGRES_URL")
    MONGO_URL = os.getenv("MONGO_URL")

    APP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
