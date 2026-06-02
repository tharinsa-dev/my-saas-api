from fastapi import FastAPI, HTTPException, Security
from fastapi.security.api_key import APIKeyHeader
import httpx

app = FastAPI()

# සල්ලි ගෙවන අයට විතරක් දෙන රහස් කෝඩ් එක
API_KEY = "tharinsa-vip-key-2026"
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

@app.get("/")
def home():
    return {"message": "Live SaaS API with Security is Active!"}

@app.get("/rate")
async def get_rate(header_key: str = Security(api_key_header)):
    if header_key != API_KEY:
        raise HTTPException(
            status_code=401, 
            detail="Invalid API Key. Please purchase a key to access live data."
        )
    
    # මේ ලින්ක් එකෙන් ලෝකේ ඇත්තම ලයිව් ඩොලර් රේට් එක ඔටෝම ඇදලා ගන්නවා
    url = "https://open.er-api.com/v6/latest/USD"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code == 200:
            data = response.json()
            # ඩොලර් එකට සාපේක්ෂව ලංකාවේ රුපියල් ගාණ (LKR Rate) ගන්නවා
            lkr_rate = data["rates"].get("LKR")
            return {
                "status": "success",
                "base": "USD",
                "target": "LKR",
                "live_rate": lkr_rate,
                "provider": "Open Exchange Rates"
            }
        else:
            raise HTTPException(status_code=500, detail="Error fetching live rates.")
