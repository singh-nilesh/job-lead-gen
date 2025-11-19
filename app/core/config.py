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
    
    MONGO_URL = os.getenv("MONGO_URL")
    MONGO_USER = os.getenv("MONGO_USER")
    MONGO_PASS = os.getenv("MONGO_PASS")
    MONGO_DB = os.getenv("MONGO_DB")

    APP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
