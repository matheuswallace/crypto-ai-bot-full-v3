# 🚀 Crypto AI Bot

Bot de análise de tendências de criptomoedas com Flask e threads paralelas.
Atualmente em **modo de simulação** (não realiza operações reais).

## 🧠 Estrutura
- `executor/`: Simula o motor de decisões.
- `ts_model/`: Modelo de tendência.
- `sentiment_model/`: Análise de sentimento.
- `web/`: Painel Flask.

## 🚀 Deploy no Render
1. Crie uma conta em [https://render.com](https://render.com)
2. Clique em **New Web Service**
3. Conecte ao seu repositório do GitHub
4. Configure:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn web.app:app`
   - Runtime: `Python 3`
5. Deploy 🎉

## 💡 Modo simulação
O bot roda localmente analisando sinais aleatórios.
Futuramente pode ser integrado com corretoras (Binance, etc.)
