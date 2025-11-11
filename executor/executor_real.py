import time
import random

def run_executor():
    print("Executor iniciado (modo simulado)...")
    while True:
        try:
            coin = random.choice(["BTC", "ETH", "SOL", "ADA"])
            signal = random.choice(["compra", "venda", "neutro"])
            print(f"[BOT] Sinal detectado para {coin}: {signal.upper()}")
            time.sleep(10)
        except Exception as e:
            print(f"Erro no executor: {e}")
            time.sleep(5)
