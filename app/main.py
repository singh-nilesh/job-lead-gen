from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.postgres.sqlalchemyConfig import engine
from app.core.config import Settings
from app.api import include_routers
from app.db.mongo.motorConfig import init_nosql_db

# initialize resources
@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup code
    from app.db.postgres.schema import Users
    print(f"Creating DB tables... in {Settings.MODE} mode")
    Users.metadata.create_all(bind=engine)

    await init_nosql_db()
    print("Main database initialized.")

    yield
    
    # shutdown code
    print("Shutting down...")
    if Settings.MODE == 'test':
        from app.db.postgres.sqlalchemyConfig import teardown_db
        print("Tearing down test database...")
        teardown_db()


# App instance
app = FastAPI(lifespan=lifespan)


# client request middleware
origin = [
    "*",
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origin,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Routes
@app.get("/health_check")
async def health_check():
    return {"status": "ok"}

'''See app/api/__init__.py for include_routers function'''
include_routers(app)


