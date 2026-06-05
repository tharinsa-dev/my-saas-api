from fastapi import FastAPI, HTTPException, Security, Query
from fastapi.security.api_key import APIKeyHeader
from fastapi.responses import HTMLResponse
import httpx

app = FastAPI()

# This is your Master Premium Key for testing. 
# RapidAPI will proxy through this or handle it via header verification.
API_KEY = "tharinsa-vip-key-2026"
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

@app.get("/", response_class=HTMLResponse)
async def home():
    html_content = """
    <!DOCTYPE html>
    <html lang="en" data-theme="dark">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>TharinsaAPI - Premium Live Currency SaaS</title>
        <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
        <style>
            :root {
                --bg-body: #0b0f19;
                --bg-container: linear-gradient(145deg, #1e293b, #0f172a);
                --bg-box: rgba(15, 23, 42, 0.6);
                --bg-input: #111827;
                --text-main: #f3f4f6;
                --text-muted: #94a3b8;
                --border: rgba(255, 255, 255, 0.08);
                --shadow: rgba(0, 0, 0, 0.5);
            }

            [data-theme="light"] {
                --bg-body: #f1f5f9;
                --bg-container: linear-gradient(145deg, #ffffff, #f8fafc);
                --bg-box: rgba(241, 245, 249, 0.8);
                --bg-input: #ffffff;
                --text-main: #0f172a;
                --text-muted: #64748b;
                --border: rgba(15, 23, 42, 0.08);
                --shadow: rgba(15, 23, 42, 0.1);
            }

            body {
                font-family: 'Plus Jakarta Sans', sans-serif;
                background-color: var(--bg-body);
                color: var(--text-main);
                margin: 0;
                padding: 0;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                min-height: 100vh;
                transition: background-color 0.3s ease, color 0.3s ease;
                position: relative;
            }
            
            .theme-toggle {
                position: absolute;
                top: 20px;
                right: 20px;
                background: var(--bg-input);
                border: 1px solid var(--border);
                color: var(--text-main);
                padding: 10px 16px;
                border-radius: 100px;
                cursor: pointer;
                font-weight: 600;
                font-size: 13px;
                display: flex;
                align-items: center;
                gap: 8px;
                box-shadow: 0 4px 12px var(--shadow);
                transition: all 0.3s ease;
            }

            .container {
                max-width: 480px;
                width: 90%;
                background: var(--bg-container);
                padding: 35px 30px;
                border-radius: 24px;
                box-shadow: 0 20px 40px var(--shadow);
                text-align: center;
                border: 1px solid var(--border);
                transition: background 0.3s ease, border 0.3s ease;
            }
            h1 { 
                font-size: 32px; 
                font-weight: 700; 
                margin-bottom: 8px; 
                background: linear-gradient(to right, #38bdf8, #818cf8);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }
            p { color: var(--text-muted); font-size: 14px; margin-bottom: 30px; line-height: 1.5; }
            .badge {
                background: rgba(14, 165, 233, 0.15);
                color: #38bdf8;
                padding: 6px 14px;
                border-radius: 100px;
                font-size: 12px;
                font-weight: 600;
                display: inline-block;
                margin-bottom: 20px;
                border: 1px solid rgba(14, 165, 233, 0.3);
            }
            .converter-box {
                background: var(--bg-box);
                padding: 25px;
                border-radius: 18px;
                border: 1px solid var(--border);
                backdrop-filter: blur(10px);
            }
            .live-indicator {
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 6px;
                font-size: 12px;
                font-weight: 700;
                color: #4ade80;
                margin-bottom: 20px;
                text-transform: uppercase;
                letter-spacing: 1px;
            }
            .dot {
                width: 8px;
                height: 8px;
                background-color: #4ade80;
                border-radius: 50%;
                animation: blink 1.5s infinite;
            }
            @keyframes blink {
                0% { opacity: 0.4; }
                50% { opacity: 1; }
                100% { opacity: 0.4; }
            }
            label { display: block; text-align: left; font-size: 11px; color: var(--text-muted); margin-bottom: 6px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; }
            
            .input-wrapper {
                display: flex;
                align-items: center;
                background: var(--bg-input);
                border: 1px solid var(--border);
                border-radius: 12px;
                padding: 4px 12px;
                margin-bottom: 20px;
                transition: all 0.3s ease;
            }
            .input-wrapper:focus-within {
                border-color: #6366f1;
                box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2);
            }
            .flag-container {
                display: flex;
                align-items: center;
                justify-content: center;
                margin-right: 12px;
                width: 24px;
            }
            .flag-img {
                width: 24px;
                height: 16px;
                object-fit: cover;
                border-radius: 2px;
            }
            select, input {
                width: 100%;
                padding: 12px 0;
                background: transparent;
                border: none;
                color: var(--text-main);
                font-size: 16px;
                box-sizing: border-box;
            }
            select:focus, input:focus {
                outline: none;
            }
            select option {
                background: var(--bg-body);
                color: var(--text-main);
            }
            .result-container {
                margin-top: 20px;
                background: linear-gradient(135deg, rgba(56, 189, 248, 0.1), rgba(129, 140, 248, 0.1));
                padding: 16px;
                border-radius: 12px;
                border: 1px solid rgba(99, 102, 241, 0.2);
            }
            .result {
                font-size: 24px;
                font-weight: 700;
                color: #2dd4bf;
            }
            .rapidapi-btn {
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 8px;
                margin-top: 25px;
                background: linear-gradient(to right, #4f46e5, #06b6d4);
                color: white;
                text-decoration: none;
                padding: 14px;
                border-radius: 12px;
                font-weight: 600;
                transition: all 0.3s ease;
                box-shadow: 0 4px 15px rgba(79, 70, 229, 0.4);
            }
            .rapidapi-btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 6px 20px rgba(79, 70, 229, 0.6);
            }
            .footer { margin-top: 25px; font-size: 11px; color: var(--text-muted); line-height: 1.6; }
        </style>
    </head>
    <body>
        <button class="theme-toggle" onclick="toggleTheme()">
            <span id="theme-icon">☀️</span> <span id="theme-text">Light Mode</span>
        </button>

        <div class="container">
            <span class="badge">🔥 100% Free Tier Available - No Credit Card Required</span>
            <h1>TharinsaAPI</h1>
            <p>Enterprise-grade real-time exchange rates for Sri Lankan Rupee (LKR).</p>
            
            <div class="converter-box">
                <div class="live-indicator">
                    <span class="dot"></span> Live Mid-Market Rates
                </div>

                <label>Select Base Currency</label>
                <div class="input-wrapper">
                    <div class="flag-container">
                        <img class="flag-img" id="baseFlag" src="https://flagcdn.com/w40/us.png">
                    </div>
                    <select id="baseCurrency" onchange="updateElements()">
                        <option value="USD" data-code="us">USD - US Dollar</option>
                        <option value="EUR" data-code="eu">EUR - Euro</option>
                        <option value="AED" data-code="ae">AED - UAE Dirham</option>
                        <option value="SAR" data-code="sa">SAR - Saudi Riyal</option>
                        <option value="INR" data-code="in">INR - Indian Rupee</option>
                        <option value="GBP" data-code="gb">GBP - British Pound</option>
                        <option value="CAD" data-code="ca">CAD - Canadian Dollar</option>
                        <option value="AUD" data-code="au">AUD - Australian Dollar</option>
                        <option value="JPY" data-code="jp">JPY - Japanese Yen</option>
                        <option value="QAR" data-code="qa">QAR - Qatari Riyal</option>
                        <option value="KWD" data-code="kw">KWD - Kuwaiti Dinar</option>
                        <option value="OMR" data-code="om">OMR - Oman Rial</option>
                        <option value="BHD" data-code="bh">BHD - Bahraini Dinar</option>
                        <option value="SGD" data-code="sg">SGD - Singapore Dollar</option>
                    </select>
                </div>

                <label>Amount</label>
                <div class="input-wrapper">
                    <div class="flag-container">
                        <img class="flag-img" id="inputFlag" src="https://flagcdn.com/w40/us.png">
                    </div>
                    <input type="number" id="amount" value="1" oninput="convertCurrency()">
                </div>

                <label>Converted Value</label>
                <div class="input-wrapper" style="margin-bottom: 0;">
                    <div class="flag-container">
                        <img class="flag-img" src="https://flagcdn.com/w40/lk.png">
                    </div>
                    <div style="width:100%;" class="result-container">
                        <div class="result" id="resultBox">Loading live rate...</div>
                    </div>
                </div>
            </div>

            <a href="https://rapidapi.com" id="rapidapiLink" target="_blank" class="rapidapi-btn">
                🚀 Subscribe on RapidAPI Hub
            </a>
            
            <div class="footer">
                Data Refresh: Automated Live Feed<br>
                Powered by Tharinsa Multi-Currency SaaS Engine
            </div>
        </div>

        <script>
            function toggleTheme() {
                const html = document.documentElement;
                const icon = document.getElementById('theme-icon');
                const text = document.getElementById('theme-text');
                
                if (html.getAttribute('data-theme') === 'dark') {
                    html.setAttribute('data-theme', 'light');
                    icon.innerText = '🌙';
                    text.innerText = 'Dark Mode';
                } else {
                    html.setAttribute('data-theme', 'dark');
                    icon.innerText = '☀️';
                    text.innerText = 'Light Mode';
                }
            }

            function updateElements() {
                const select = document.getElementById('baseCurrency');
                const selectedOption = select.options[select.selectedIndex];
                const code = selectedOption.getAttribute('data-code');
                
                document.getElementById('baseFlag').src = `https://flagcdn.com/w40/${code}.png`;
                document.getElementById('inputFlag').src = `https://flagcdn.com/w40/${code}.png`;
                
                convertCurrency();
            }

            async function convertCurrency() {
                const base = document.getElementById('baseCurrency').value;
                const amount = document.getElementById('amount').value || 1;
                const resultBox = document.getElementById('resultBox');
                
                try {
                    const response = await fetch(`https://open.er-api.com/v6/latest/${base}`);
                    const data = await response.json();
                    const lkrRate = data.rates.LKR;
                    const finalAmount = (lkrRate * amount).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2});
                    
                    resultBox.innerText = `${finalAmount} LKR`;
                } catch (error) {
                    resultBox.innerText = "Error loading rates.";
                }
            }
            window.onload = updateElements;
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
    if header_key != API_KEY:
        raise HTTPException(
            status_code=401, 
            detail="Invalid API Key. Please subscribe on RapidAPI to get a valid token."
        )
    
    base_upper = base.upper()
    supported = ["USD", "EUR", "AED", "SAR", "INR", "GBP", "CAD", "AUD", "JPY", "QAR", "KWD", "OMR", "BHD", "SGD"]
    
    if base_upper not in supported:
        raise HTTPException(
            status_code=400, 
            detail=f"Currency '{base_upper}' is not supported yet. Supported: {supported}"
        )
    
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
                "provider": "Tharinsa SaaS Engine Engine v2",
                "last_update": data.get("time_last_update_utc")
            }
        else:
            raise HTTPException(status_code=500, detail="Error fetching data from live provider.")
