from indicators import calculate_indicators


from indicators import calculate_indicators

def analyze_market(df):

    df = calculate_indicators(df)
    last = df.iloc[-1]

    bull = 0
    bear = 0
    reasons = []

    # EMA
    if last["EMA9"] > last["EMA21"]:
        bull += 35
        reasons.append("EMA Alcista")
    else:
        bear += 35
        reasons.append("EMA Bajista")

    # RSI
    if last["RSI"] >= 60:
        bull += 20
        reasons.append("RSI Alcista")
    elif last["RSI"] <= 40:
        bear += 20
        reasons.append("RSI Bajista")
    else:
        reasons.append("RSI Neutral")

    # MACD
    if last["MACD"] > last["MACD_SIGNAL"]:
        bull += 30
        reasons.append("MACD Compra")
    else:
        bear += 30
        reasons.append("MACD Venta")

    # Volumen
    if last["Volume"] > last["VOL_AVG"]:
        bull += 15
        bear += 15
        reasons.append("Volumen Alto")
    else:
        reasons.append("Volumen Bajo")

    if bull > bear:
        confidence = bull
        prediction = "UP"
    elif bear > bull:
        confidence = bear
        prediction = "DOWN"
    else:
        confidence = 50
        prediction = "NO OPERAR"

    if confidence < 60:
        prediction = "NO OPERAR"

    confidence = min(confidence, 100)

    return {
        "prediction": prediction,
        "confidence": confidence,
        "reasons": reasons,
        "price": float(last["Close"]),
        "ema9": round(float(last["EMA9"]), 2),
        "ema21": round(float(last["EMA21"]), 2),
        "rsi": round(float(last["RSI"]), 2),
        "macd": round(float(last["MACD"]), 2),
    }