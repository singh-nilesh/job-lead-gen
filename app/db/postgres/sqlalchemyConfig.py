''' 
Configuration file for SQLAlchemy ORM
- databse: PostgreSQL for production
- SQLite in-memory for tests
- Usage: Authentication
'''

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import Settings


# Use different database URL for tests
if Settings.MODE == 'test':
    SQLALCHEMY_DATABASE_URL = "sqlite:///file::memory:?cache=shared"
else:
    SQLALCHEMY_DATABASE_URL = Settings.POSTGRES_URL

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False} if Settings.MODE == 'test' else {},
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)

# single Base for all models to inherit
Base = declarative_base()

# Dependency to get DB session
def get_auth_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def teardown_db():
    """ Drop all tables - for test cleanup """
    Base.metadata.drop_all(bind=engine)
