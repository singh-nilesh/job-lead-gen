from fastapi import FastAPI
import uvicorn


def main():
    print("Starting the application...")
    uvicorn.run("main:app", host="0.0.0.0", port=8000)

app = FastAPI()

@app.get("/health_check")
async def health_check():
    return {"status": "ok"}


if __name__ == "__main__":
    main()