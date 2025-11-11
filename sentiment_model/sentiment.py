def analyze_sentiment(text):
    text = text.lower()
    if "queda" in text or "baixa" in text:
        return "negativo"
    elif "alta" in text or "subida" in text:
        return "positivo"
    else:
        return "neutro"
