import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify

app = Flask(__name__)

def get_lowest_price():
    url = "https://csfloat.com/search?sort_by=lowest_price&def_index=4726"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')
        price_element = soup.find('div', class_='price-class')

        if price_element:
            lowest_price = price_element.get_text(strip=True)
            return f"Lowest price: {lowest_price}"
        else:
            return "Price not found"
    else:
        return "Error fetching price"

@app.route('/csfloat')
def csfloat_price():
    return jsonify({"lowest_price": get_lowest_price()})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)