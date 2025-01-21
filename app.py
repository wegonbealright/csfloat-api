import requests
from flask import Flask, jsonify

app = Flask(__name__)

def get_lowest_price():
    url = "https://csfloat.com/search?sort_by=lowest_price&def_index=4726"
    response = requests.get(url)
    if response.status_code == 200:
        # Extract the lowest price from the response (adjust this parsing logic)
        return "Lowest price: $XX.XX"
    return "Error fetching price"

@app.route('/csfloat')
def csfloat_price():
    return jsonify({"lowest_price": get_lowest_price()})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
