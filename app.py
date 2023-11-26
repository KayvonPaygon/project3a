from flask import Flask, render_template, request
from data_methods import *
import os
import datetime
import csv

app = Flask(__name__)

# Alpha Vantage API key
api_key = '8FCYBQQE0XDXJWDC'

# Load stock symbols from stocks.csv
stocks = []
with open('stocks.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        stocks.append(row['Symbol'])

@app.route('/', methods=['GET', 'POST'])
def index():
    chart_path = None

    if request.method == 'POST':
        stock_symbol = request.form['stock_symbol']
        chart_choice = request.form['chart_choice']
        time_series_choice = request.form['time_series_choice']
        start_date = request.form['start_date']
        end_date = request.form['end_date']

        try:
            check_start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
            check_end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")

            if check_end_date < check_start_date:
                error = "End date cannot be before the begin date."
                return render_template('index.html', stocks=stocks, error=error)

            time_series_functions = {
                '1': 'TIME_SERIES_INTRADAY',
                '2': 'TIME_SERIES_DAILY',
                '3': 'TIME_SERIES_WEEKLY',
                '4': 'TIME_SERIES_MONTHLY'
            }

            time_series_function = time_series_functions.get(time_series_choice, 'TIME_SERIES_DAILY')

            data = retrieve_data(time_series_function, stock_symbol, api_key, start_date, end_date)
            chart = generate_chart(data, chart_choice, time_series_function)

            chart.render_to_file('static/chart.svg')
            chart_path = os.path.abspath('static/chart.svg')

            return render_template('index.html', stocks=stocks, chart_path=chart_path)

        except ValueError:
            error = "Invalid date format. Please use YYYY-MM-DD format for the dates."
            return render_template('index.html', stocks=stocks, error=error)

    return render_template('index.html', stocks=stocks, chart_path=chart_path)

if __name__ == '__main__':
    app.run(debug=True)
