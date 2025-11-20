import os
from dotenv import load_dotenv
from typing import Literal, cast

# load .env into os.environ at import time
load_dotenv()

class Settings:
    MODE: Literal['prod','dev','test'] = cast(Literal['prod','dev','test'], os.getenv("MODE", "dev"))
    
    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM = os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES:int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "10"))

    POSTGRES_URL = os.getenv("POSTGRES_URL")
    
    MONGO_APP_USER = os.getenv("APP_USER")
    MONGO_APP_PASS = os.getenv("APP_PASSWORD")
    MONGO_DB = os.getenv("MONGO_DB")
    
    MONGO_URL = f"mongodb://{MONGO_APP_USER}:{MONGO_APP_PASS}@mongodb-service:27017/{MONGO_DB}?authSource={MONGO_DB}"

    APP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
