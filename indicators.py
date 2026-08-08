import pandas as pd
from ta.trend import EMAIndicator, MACD
from ta.momentum import RSIIndicator


def calculate_indicators(df):

    data = df.copy()

    # Si Yahoo devuelve columnas MultiIndex, las aplana
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    data = data.dropna()

    # EMA
    data["EMA9"] = EMAIndicator(
        close=data["Close"],
        window=9
    ).ema_indicator()

    data["EMA21"] = EMAIndicator(
        close=data["Close"],
        window=21
    ).ema_indicator()

    # RSI
    data["RSI"] = RSIIndicator(
        close=data["Close"],
        window=14
    ).rsi()

    # MACD
    macd = MACD(data["Close"])

    data["MACD"] = macd.macd()

    data["MACD_SIGNAL"] = macd.macd_signal()

    # Volumen promedio
    data["VOL_AVG"] = data["Volume"].rolling(20).mean()

    return data