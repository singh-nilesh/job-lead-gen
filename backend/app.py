from fastapi import FastAPI

app = FastAPI()

# Test endpoint to verify the application is running
@app.get("/health")
async def health_check():
    return {"status": "ok"}

