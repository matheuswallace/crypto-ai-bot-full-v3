import os
import sys
import threading
from flask import Flask, render_template, jsonify

# Adiciona o caminho raiz do projeto
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from executor.executor_real import run_executor

app = Flask(__name__)

@app.before_request
def start_executor_once():
    if not getattr(app, "_executor_started", False):
        executor_thread = threading.Thread(target=run_executor)
        executor_thread.daemon = True
        executor_thread.start()
        app._executor_started = True

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/status")
def status():
    return jsonify({"status": "Bot rodando no modo simulação", "success": True})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
