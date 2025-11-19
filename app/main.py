from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.sqlalchemyConfig import engine
from app.core.config import Settings
from app.api import include_routers

# initialize resources
@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup code
    from app.db import schema
    print(f"Creating DB tables... in {Settings.MODE} mode")
    schema.Base.metadata.create_all(bind=engine)

    yield
    
    # shutdown code
    print("Shutting down...")
    if Settings.MODE == 'test':
        from app.db.sqlalchemyConfig import teardown_db
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


