from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

app = Flask(__name__)

def get_first_lowest_price():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    try:
        url = "https://csfloat.com/search?sort_by=lowest_price&def_index=4726"
        driver.get(url)

        time.sleep(5)

        price_element = driver.find_element(By.CSS_SELECTOR, "div.price.ng-star-inserted")
        first_price = price_element.text.strip()

        return f"First lowest price: {first_price}"

    except Exception as e:
        return f"Error fetching price: {str(e)}"

    finally:
        driver.quit()

@app.route('/csfloat')
def csfloat_price():
    return jsonify({"lowest_price": get_first_lowest_price()})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)