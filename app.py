import requests
from flask import Flask, jsonify

app = Flask(__name__)

CSFLOAT_API_URL = "https://csfloat.com/api/v1/listings"

def get_lowest_price():
    params = {
        "limit": 40,
        "sort_by": "lowest_price",
        "def_index": 4726
    }

    headers = {
        "Authorization": "F40li3QQ91-4HnGf4c1HDRqxgd-RxKWG",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
        "Accept": "application/json",
        "Referer": "https://csfloat.com/"
    }

    try:
        response = requests.get(CSFLOAT_API_URL, headers=headers, params=params)
        response.raise_for_status()

        data = response.json()

        if "data" in data and len(data["data"]) > 0:
            first_item = data["data"][0]
            price_cents = first_item.get('price', 0)

            if isinstance(price_cents, (int, float)):
                price_usd = price_cents / 100
                price_eur = convert_usd_to_eur(price_usd)
                return {"price_eur": price_eur}
            else:
                return {"error": "Invalid price format from API"}

        return {"error": "No listings found"}

    except requests.exceptions.RequestException as e:
        return {"error": f"Failed to fetch CSFloat data: {str(e)}"}

def convert_usd_to_eur(usd_amount):
    exchange_api_url = "https://api.exchangerate-api.com/v4/latest/USD"

    try:
        response = requests.get(exchange_api_url)
        response.raise_for_status()
        exchange_data = response.json()

        eur_rate = float(exchange_data["rates"]["EUR"])
        eur_amount = usd_amount * eur_rate
        return f"{eur_amount:.2f}"

    except requests.exceptions.RequestException as e:
        return f"Error fetching exchange rate: {str(e)}"

@app.route('/csfloat_price')
def csfloat_price():
    lowest_price = get_lowest_price()
    return jsonify(lowest_price)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
