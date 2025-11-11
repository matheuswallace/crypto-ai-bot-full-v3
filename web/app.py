import os
import sys
import threading
from flask import Flask, jsonify, render_template
from datetime import datetime

# Corrige caminho de importação
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from executor.executor_real import run_executor

app = Flask(__name__)
logs = []  # Aqui os logs são armazenados na memória

def add_log(message):
    """Adiciona logs com timestamp"""
    logs.append(f"[{datetime.now().strftime('%H:%M:%S')}] {message}")
    if len(logs) > 500:
        logs.pop(0)

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
    if not getattr(app, "_executor_started", False):
        executor_thread = threading.Thread(target=executor_with_logs)
        executor_thread.daemon = True
        executor_thread.start()
        app._executor_started = True

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
