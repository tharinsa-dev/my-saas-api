from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "SaaS API is running successfully!"}

@app.get("/rate")
def get_rate():
    return {
        "status": "success",
        "currency": "LKR",
        "rate": 300.50
    }
