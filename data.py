import requests
import yfinance as yf


def get_btc_price():
    """
    Obtiene el precio spot actual de BTC desde Coinbase.
    """

    try:

        url = "https://api.coinbase.com/v2/prices/spot?currency=USD"

        response = requests.get(url, timeout=10)

        response.raise_for_status()

        data = response.json()

        return float(data["data"]["amount"])

    except Exception as e:

        print("ERROR PRECIO:", e)

        return None


def get_market_data():
    """
    Descarga las últimas velas BTCUSD de 15 minutos.
    """

    try:

        df = yf.download(
            tickers="BTC-USD",
            period="5d",
            interval="15m",
            progress=False,
            auto_adjust=False
        )

        if df.empty:

            return None

        return df.reset_index()

    except Exception as e:

        print("ERROR MARKET:", e)

        return None