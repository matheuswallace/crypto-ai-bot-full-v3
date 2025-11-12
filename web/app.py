import os
import sys
import threading
from flask import Flask, jsonify, render_template
from datetime import datetime
from web.db import log_to_db


# Corrige caminho de importação
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from executor.executor_real import run_executor

import time

executor_thread = None

def monitor_executor():
    global executor_thread
    while True:
        if executor_thread is None or not executor_thread.is_alive():
            add_log("Executor parado — reiniciando automaticamente ♻️")
            executor_thread = threading.Thread(target=executor_with_logs)
            executor_thread.daemon = True
            executor_thread.start()
        time.sleep(10)  # checa a cada 10 segundos


app = Flask(__name__)
logs = []  # Aqui os logs são armazenados na memória

def add_log(message):
    logs.append(f"[{datetime.now().strftime('%H:%M:%S')}] {message}")
    if len(logs) > 500:
        logs.pop(0)
    try:
        log_to_db(message)
    except Exception as e:
        print(f"Erro ao salvar log no banco: {e}")


def executor_with_logs():
    add_log("Executor iniciado 🚀")
    try:
        run_executor(log_callback=add_log)
    except Exception as e:
        add_log(f"Erro: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/logs')
def show_logs():
    return render_template('logs.html')

@app.route('/api/logs')
def api_logs():
    """Retorna os logs em JSON (usado pela página de visualização)"""
    return jsonify(logs)


@app.before_request
def start_executor_once():
    global executor_thread
    if not getattr(app, "_executor_started", False):
        add_log("Iniciando executor principal e watchdog 👀")
        executor_thread = threading.Thread(target=executor_with_logs)
        executor_thread.daemon = True
        executor_thread.start()

        # Inicia o watchdog
        watchdog_thread = threading.Thread(target=monitor_executor)
        watchdog_thread.daemon = True
        watchdog_thread.start()

        app._executor_started = True


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
