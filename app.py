from flask import Flask, jsonify, render_template
from datetime import datetime

from data import get_btc_price, get_market_data
from strategy import analyze_market

app = Flask(__name__)


def next_candle():

    now = datetime.now()

    minute = ((now.minute // 15) + 1) * 15

    if minute >= 60:

        nxt = now.replace(
            hour=(now.hour + 1) % 24,
            minute=0,
            second=0,
            microsecond=0
        )

    else:

        nxt = now.replace(
            minute=minute,
            second=0,
            microsecond=0
        )

    remaining = nxt - now

    total = int(remaining.total_seconds())

    return f"{total//60:02d}:{total%60:02d}"

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