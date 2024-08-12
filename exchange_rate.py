from flask import Flask, render_template, request
import pandas as pd
import requests
import io

app = Flask(__name__)

# Function to fetch exchange rate data
def get_exchange_rates():
    url = "https://nbs.sk/export/sk/exchange-rate/latest/csv"
    response = requests.get(url)
    response.raise_for_status()
    csv_data = io.StringIO(response.text)
    exchange_rates = pd.read_csv(csv_data, delimiter=';')
    return exchange_rates

@app.route('/', methods=['GET', 'POST'])
def index():
    exchange_rate = None
    currency_code = None
    error = None
     
    if request.method == 'POST':
        currency_code = request.form['currency'].upper()
        exchange_rates = get_exchange_rates()

        for label, content in exchange_rates.items():
            if label == currency_code:
                exchange_rate = content[0]

    return render_template('index.html', exchange_rate=exchange_rate, currency_code=currency_code, error=error)

if __name__ == '__main__':
    app.run(debug=True)
