import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.sqlalchemyConfig import engine, Base
from app.api import include_routers

app = FastAPI()

# origin
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

# initialize resources
@app.on_event("startup")
async def startup_event():

    print("Creating Users tables...")
    from app.db import schema
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully.")


# Routes
@app.get("/health_check")
async def health_check():
    return {"status": "ok"}

'''See app/api/__init__.py for include_routers function'''
include_routers(app)


