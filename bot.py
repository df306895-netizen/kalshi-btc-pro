from flask import Flask, render_template
from datetime import datetime
import ccxt
import pandas as pd
import ta

app = Flask(__name__)

exchange = ccxt.coinbase()

@app.route("/")
def index():

    try:

        velas = exchange.fetch_ohlcv(
            "BTC/USD",
            timeframe="15m",
            limit=200
        )

        df = pd.DataFrame(
            velas,
            columns=[
                "time",
                "open",
                "high",
                "low",
                "close",
                "volume"
            ]
        )

        # ==========================
        # INDICADORES
        # ==========================

        df["EMA9"] = ta.trend.EMAIndicator(
            df["close"],
            window=9
        ).ema_indicator()

        df["EMA21"] = ta.trend.EMAIndicator(
            df["close"],
            window=21
        ).ema_indicator()

        df["EMA50"] = ta.trend.EMAIndicator(
            df["close"],
            window=50
        ).ema_indicator()

        df["RSI"] = ta.momentum.RSIIndicator(
            df["close"],
            window=14
        ).rsi()

        macd = ta.trend.MACD(df["close"])

        df["MACD"] = macd.macd()
        df["SIGNAL"] = macd.macd_signal()

        adx = ta.trend.ADXIndicator(
            high=df["high"],
            low=df["low"],
            close=df["close"],
            window=14
        )

        df["ADX"] = adx.adx()

        ultimo = df.iloc[-1]

        # ==========================
        # SCORE
        # ==========================

        score = 0

        # EMA 9 vs EMA21

        if ultimo["EMA9"] > ultimo["EMA21"]:
            score += 25
        else:
            score -= 25

        # Precio vs EMA50

        if ultimo["close"] > ultimo["EMA50"]:
            score += 20
        else:
            score -= 20

        # RSI

        if ultimo["RSI"] > 55:
            score += 15

        elif ultimo["RSI"] < 45:
            score -= 15

        # MACD

        if ultimo["MACD"] > ultimo["SIGNAL"]:
            score += 20
        else:
            score -= 20

        # ADX

        if ultimo["ADX"] > 25:
            score += 20

        confianza = min(100, abs(score))

        # ==========================
        # FILTRO NO OPERAR
        # ==========================

        if ultimo["ADX"] < 20:

            senal = "NO OPERAR"
            color = "#ffcc00"

        elif score >= 60:

            senal = "UP"
            color = "#00ff66"

        elif score <= -60:

            senal = "DOWN"
            color = "#ff2d55"

        else:

            senal = "NO OPERAR"
            color = "#ffcc00"

        # ==========================
        # CONTADOR VELA
        # ==========================

        ahora = datetime.now()

        minutos_restantes = 14 - (ahora.minute % 15)
        segundos_restantes = 59 - ahora.second

        contador = f"{minutos_restantes:02d}:{segundos_restantes:02d}"

        return render_template(

            "index.html",

            precio=f"{ultimo['close']:,.2f}",

            senal=senal,

            color=color,

            confianza=confianza,

            contador=contador

        )

    except Exception as e:

        return f"<h2>Error</h2><pre>{e}</pre>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)