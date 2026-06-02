from fastapi import FastAPI, HTTPException, Security, Query
from fastapi.security.api_key import APIKeyHeader
import httpx

app = FastAPI()

# VIP පාරිභෝගිකයන් සඳහා රහස් කෝඩ් එක
API_KEY = "tharinsa-vip-key-2026"
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

@app.get("/")
def home():
    return {
        "message": "Welcome to Tharinsa's Multi-Currency Live SaaS API!",
        "supported_currencies": ["USD", "EUR", "AED", "SAR", "INR", "GBP"],
        "endpoint": "/rate?base=USD"
    }

@app.get("/rate")
async def get_rate(
    base: str = Query("USD", description="Base currency (e.g., USD, EUR, AED)"),
    header_key: str = Security(api_key_header)
):
    # ආරක්ෂක පද්ධතිය චෙක් කිරීම
    if header_key != API_KEY:
        raise HTTPException(
            status_code=401, 
            detail="Invalid API Key. Please purchase a premium key to access multi-currency live data."
        )
    
    base_upper = base.upper()
    supported = ["USD", "EUR", "AED", "SAR", "INR", "GBP"]
    
    if base_upper not in supported:
        raise HTTPException(
            status_code=400, 
            detail=f"Currency '{base_upper}' is not supported yet. Supported: {supported}"
        )
    
    # ලයිව් ඩේටා ලබාගන්නා ලින්ක් එක
    url = f"https://open.er-api.com/v6/latest/{base_upper}"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code == 200:
            data = response.json()
            lkr_rate = data["rates"].get("LKR")
            return {
                "status": "success",
                "base_currency": base_upper,
                "target_currency": "LKR",
                "live_rate": lkr_rate,
                "provider": "Open Exchange Rates",
                "last_update": data.get("time_last_update_utc")
            }
        else:
            raise HTTPException(status_code=500, detail="Error fetching data from live provider.")
