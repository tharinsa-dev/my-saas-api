from fastapi import FastAPI, HTTPException, Security
from fastapi.security.api_key import APIKeyHeader

app = FastAPI()

# අපේ රහස් API Key එක (මේක තියෙන අයට විතරයි ඩේටා පේන්නේ)
API_KEY = "tharinsa-vip-key-2026"
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

@app.get("/")
def home():
    return {"message": "SaaS API Security System Active!"}

@app.get("/rate")
def get_rate(header_key: str = Security(api_key_header)):
    # කෙනෙක් දෙන API Key එක අපේ Key එකට සමානද බලනවා
    if header_key == API_KEY:
        return {
            "status": "success",
            "currency": "LKR",
            "rate": 300.50
        }
    else:
        # Key එක වැරදි නම් හෝ නැත්නම් සල්ලි ගෙවන්න කියලා පෙන්වනවා
        raise HTTPException(
            status_code=401, 
            detail="Invalid API Key. Please purchase a key to access data."
        )
