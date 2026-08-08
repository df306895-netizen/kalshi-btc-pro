from datetime import datetime, timedelta
from flask import Flask, jsonify, render_template


from data import get_btc_price, get_market_data
from strategy import analyze_market

app = Flask(__name__)

def next_candle():
    now = datetime.now()

    minutes_to_add = 15 - (now.minute % 15)
    if minutes_to_add == 15 and now.second == 0:
        minutes_to_add = 0

    nxt = (
        now.replace(second=0, microsecond=0)
        + timedelta(minutes=minutes_to_add)
    )

    total = max(0, int((nxt - now).total_seconds()))

    minutes = total // 60
    seconds = total % 60

    return f"{minutes:02d}:{seconds:02d}"

@app.route("/api/signal")
def api_signal():

    price = get_btc_price()

    market = get_market_data()

    if market is None:

        return jsonify({
            "price": price,
            "prediction": "SIN DATOS",
            "confidence": 0,
            "ema9": 0,
            "ema21": 0,
            "rsi": 0,
            "macd": 0,
            "reasons": [],
            "countdown": next_candle()
        })

    signal = analyze_market(market)

    signal["price"] = price

    signal["countdown"] = next_candle()

    return jsonify(signal)
@app.route("/")
def index():

    return render_template("index.html")


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
