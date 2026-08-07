from indicators import calculate_indicators


def analyze_market(df):

    df = calculate_indicators(df)

    last = df.iloc[-1]

    score = 0
    reasons = []

    # ==========================
    # EMA
    # ==========================
    if last["EMA9"] > last["EMA21"]:
        score += 35
        reasons.append("EMA9 arriba de EMA21")
    else:
        score -= 35
        reasons.append("EMA9 debajo de EMA21")

    # ==========================
    # RSI
    # ==========================
    if last["RSI"] >= 55:
        score += 15
        reasons.append("RSI Alcista")
    elif last["RSI"] <= 45:
        score -= 15
        reasons.append("RSI Bajista")
    else:
        reasons.append("RSI Neutral")

    # ==========================
    # MACD
    # ==========================
    if last["MACD"] > last["MACD_SIGNAL"] and last["MACD"] > 0:
        score += 35
        reasons.append("MACD Compra Confirmada")

    elif last["MACD"] < last["MACD_SIGNAL"] and last["MACD"] < 0:
        score -= 35
        reasons.append("MACD Venta Confirmada")

    else:
        reasons.append("MACD Neutral")

    # ==========================
    # VOLUMEN
    # ==========================
    if last["Volume"] > last["VOL_AVG"]:
        score += 15
        reasons.append("Volumen Alto")
    else:
        score -= 15
        reasons.append("Volumen Bajo")

    # ==========================
    # CONFIANZA
    # ==========================
    confidence = int((score + 100) / 2)
    confidence = max(0, min(confidence, 100))

    # ==========================
    # PREDICCIÓN
    # ==========================
    if confidence < 50:
        prediction = "NO OPERAR"
    else:
        if score >= 0:
            prediction = "UP"
        else:
            prediction = "DOWN"

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