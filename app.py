from fastapi import FastAPI, HTTPException, Security, Query
from fastapi.security.api_key import APIKeyHeader
from fastapi.responses import HTMLResponse
import httpx

app = FastAPI()

# VIP පාරිභෝගිකයන් සඳහා රහස් කෝඩ් එක
API_KEY = "tharinsa-vip-key-2026"
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

@app.get("/", response_class=HTMLResponse)
async def home():
    # සර් කියපු විදිහට ලෑන්ඩ් වෙනකොටම ලයිව් කරන්සි ඔක්කොම බලන්න පුළුවන් සුපිරි Landing Page එක
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>TharinsaAPI - Live LKR Exchange Rates</title>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
        <style>
            body {
                font-family: 'Inter', sans-serif;
                background-color: #0f172a;
                color: #f8fafc;
                margin: 0;
                padding: 0;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                min-height: 100vh;
            }
            .container {
                max-width: 500px;
                width: 90%;
                background: #1e293b;
                padding: 30px;
                border-radius: 16px;
                box-shadow: 0 10px 25px rgba(0,0,0,0.3);
                text-align: center;
                border: 1px solid #334155;
            }
            h1 { font-size: 28px; margin-bottom: 10px; color: #38bdf8; }
            p { color: #94a3b8; font-size: 15px; margin-bottom: 25px; }
            .badge {
                background-color: #0ea5e9;
                color: white;
                padding: 6px 12px;
                border-radius: 20px;
                font-size: 12px;
                font-weight: 600;
                display: inline-block;
                margin-bottom: 20px;
            }
            .converter-box {
                background: #0f172a;
                padding: 20px;
                border-radius: 12px;
                border: 1px solid #334155;
            }
            label { display: block; text-align: left; font-size: 13px; color: #94a3b8; margin-bottom: 5px; font-weight: 600; }
            select, input {
                width: 100%;
                padding: 12px;
                background: #1e293b;
                border: 1px solid #475569;
                border-radius: 8px;
                color: white;
                font-size: 16px;
                margin-bottom: 15px;
                box-sizing: border-box;
            }
            .result {
                font-size: 22px;
                font-weight: 700;
                color: #4ade80;
                margin-top: 15px;
                background: rgba(74, 222, 128, 0.1);
                padding: 12px;
                border-radius: 8px;
            }
            .footer { margin-top: 20px; font-size: 12px; color: #64748b; }
        </style>
    </head>
    <body>
        <div class="container">
            <span class="badge">🔥 100% Free Tier Available - No Credit Card Required</span>
            <h1>TharinsaAPI</h1>
            <p>Real-time Mid-Market Exchange Rates for Sri Lankan Rupee (LKR)</p>
            
            <div class="converter-box">
                <label>Select Base Currency:</label>
                <select id="baseCurrency" onchange="convertCurrency()">
                    <option value="USD">USD - US Dollar</option>
                    <option value="EUR">EUR - Euro</option>
                    <option value="AED">AED - UAE Dirham</option>
                    <option value="SAR">SAR - Saudi Riyal</option>
                    <option value="INR">INR - Indian Rupee</option>
                    <option value="GBP">GBP - British Pound</option>
                </select>

                <label>Amount:</label>
                <input type="number" id="amount" value="1" oninput="convertCurrency()">

                <label>Converted Amount in LKR:</label>
                <div class="result" id="resultBox">Loading live rate...</div>
            </div>
            
            <div class="footer">
                Data Source: Open Exchange Rates network<br>
                Rate Type: Mid-Market Average Rate
            </div>
        </div>

        <script>
            async function convertCurrency() {
                const base = document.getElementById('baseCurrency').value;
                const amount = document.getElementById('amount').value || 1;
                const resultBox = document.getElementById('resultBox');
                
                try {
                    // Open-API එකෙන් කෙළින්ම ලයිව් ඩේටා ඇදලා UI එකට දෙනවා (Key එකක් නැති අයට බලාගන්න)
                    const response = await fetch(`https://open.er-api.com/v6/latest/${base}`);
                    const data = await response.json();
                    const lkrRate = data.rates.LKR;
                    const finalAmount = (lkrRate * amount).toFixed(2);
                    
                    resultBox.innerText = `${amount} ${base} = ${finalAmount} LKR`;
                } catch (error) {
                    resultBox.innerText = "Error loading rates.";
                }
            }
            // පේජ් එක ලෝඩ් වෙද්දීම රන් වෙන්න
            window.onload = convertCurrency;
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)

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
