from flask import Flask, render_template, request
import requests
import pygal

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=('GET', 'POST'))
def index():
    
    error_message = None
    
    if request.method == 'POST':
        stock_symbol = request.form['stock_symbol']
        chart_type = request.form['chart_type']
        time_series = request.form['time_series']
        start_date = request.form['start_date']
        end_date = request.form['end_date']

        try:
            if time_series == "1":
                url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&outputsize=full&symbol={stock_symbol}&apikey=Y7P82MTGYSOW6CEX"
            elif time_series == "2":
                url = f"https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol={stock_symbol}&apikey=Y7P82MTGYSOW6CEX"
            elif time_series == "3":
                url = f"https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol={stock_symbol}&apikey=Y7P82MTGYSOW6CEX"
            else:
                raise Exception("Error: invalid time series function")

            try:
                get_url = requests.get(url)
                get_url.raise_for_status()
            except requests.exceptions.HTTPError as e:
                raise Exception(f"Error retrieving data: {e}")

            stock_data = get_url.json()
            if len(stock_data.keys()) < 2:
                raise Exception("Error: no stock data found")

            stock_key = list(stock_data.keys())[1]

            data = stock_data[stock_key]

            data_dict = {}

            for date, values in data.items():
                if start_date <= date <= end_date:
                    data_dict[date] = values

            sorted_data = sorted(data_dict.items())

            if chart_type == "1":
                chart = pygal.Line(x_label_rotation=30, show_minor_x_labels=True)
            elif chart_type == "2":
                chart = pygal.Bar(x_label_rotation=30, show_minor_x_labels=True)
            else:
                raise Exception("Error: invalid chart type")

            chart.title = f"{stock_symbol} Stock: {start_date} to {end_date}"
            chart.x_labels = [date for date, value in sorted_data]
            chart.add("Open", [float(value["1. open"]) for date, value in sorted_data])
            chart.add("High", [float(value["2. high"])for date, value in sorted_data])
            chart.add("Low", [float(value["3. low"]) for date, value in sorted_data])
            chart.add("Close", [float(value["4. close"]) for date, value in sorted_data])

            chart = chart.render_data_uri()

            return render_template("index.html", chart=chart)

        except Exception as e:
            error_message = str(e)

    return render_template("index.html", error_message=error_message)

app.run()

