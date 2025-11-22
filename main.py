import os
import telebot
from flask import Flask, request

# Pega o token do Render (variável de ambiente)
TOKEN = os.environ.get("BOT_TOKEN")

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# -------------------------------
# COMANDOS DO BOT
# -------------------------------
@bot.message_handler(commands=['start'])
def start(msg):
    bot.reply_to(msg, "Olá! Eu sou um bot rodando no Render 👋")

@bot.message_handler(commands=['bom_dia'])
def bom_dia(msg):
    bot.reply_to(msg, "Bom diaaa 🌞")

# -------------------------------
# WEBHOOK
# -------------------------------

@app.route('/', methods=['GET'])
def home():
    return "Bot ativo!"

@app.route('/webhook', methods=['POST'])
def webhook():
    update_json = request.stream.read().decode("utf-8")
    update = telebot.types.Update.de_json(update_json)
    bot.process_new_updates([update])
    return "OK", 200

# Registrar webhook ao iniciar no Render
@app.before_first_request
def set_webhook():
    webhook_url = os.environ.get("WEBHOOK_URL")
    bot.remove_webhook()
    bot.set_webhook(url=webhook_url)

# Iniciar o Flask
if __name__ == "_main_":
    app.run(host="0.0.0.0", port=10000)