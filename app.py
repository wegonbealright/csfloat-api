import aiohttp
import asyncio
from flask import Flask, jsonify

app = Flask(__name__)

async def fetch_price():
    url = "https://csfloat.com/search?sort_by=lowest_price&def_index=4726"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            text = await response.text()
            soup = BeautifulSoup(text, 'html.parser')
            price_element = soup.find('div', class_='price ng-star-inserted')
            return price_element.get_text(strip=True) if price_element else "Price not found"

@app.route('/csfloat')
async def csfloat_price():
    price = await fetch_price()
    return jsonify({"lowest_price": price})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
