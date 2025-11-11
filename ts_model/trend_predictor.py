def predict_trend(data):
    return "alta" if sum(data[-3:]) > sum(data[:3]) else "baixa"
