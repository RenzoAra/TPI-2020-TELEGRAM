import logging
import os
import telegram
import random
import sys
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

#configurar loggin

logging.basicConfig(
    level= logging.INFO, format="%(asctime)s-%(name)s-%(levelname)s-%(message)s,"
)
logger = logging.getLogger()

#solicitar token

TOKEN = os.getenv("TOKEN")
mode = os.getenv("MODE")

if mode == 'dev':
    #acceso local (desarrollo)
    def run (updater):
        updater.start_polling()
        print("BOT CARGADO")
        updater.idle() #permite finalizar el bot con "ctrl + c"

elif mode == "prod":
    #acceso HEROKU
    def run(updater):
        PORT = int(os.environ.get("PORT","8443"))
        HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME")
        #code from https://github.com/python-telegram-bot/python-telegram-bot/wiki/Webhooks#heroku
        updater.start_webhook(listen = "0.0.0.0", port = PORT , url_path = TOKEN)
        updater.bot.set_webhook(f"https://{HEROKU_APP_NAME}.herokuapp.com/{TOKEN}")

else:
    logger.info("No se especifico el MODE")
    sys.exit()


def start(update,context):
    logger.info(f"El usuario {update.effective_user['username']}, ha iniciado una conversacion")
    name = update.effective_user['first_name']
    update.message.reply_text(f"Hola {name} yo soy tu bot.")

def random_number(update,context):
    user_id = update.effective_user['id']
    logger.info(f"El {user_id}, ha solicitado un numero aleatorio")
    number = random.randint(0,10)
    context.bot.sendMessage(chat_id = user_id, parse_mode="HTML", text=f"<b>Numero</b> aleatorio:\n{number}")

def echo(update,context):
    user_id = update.effective_user['id']
    logger.info(f"El {user_id}, ha enviado un mensaje de texto")
    text = update.message.text
    context.bot.sendMessage (
        chat_id = user_id,
        parse_mode = "MarkdownV2",
        text = f"*Escribiste*\n_{text}_"
    )


if __name__ == "__main__":
    #obtenemos informacion de nuestro bot
    my_bot = telegram.Bot(token = TOKEN)
    #print (my_bot.getMe())

#enlazamos nuestro updater con nuestro bot a traves del token

updater = Updater(my_bot.token, use_context=True)

#creamos un despachador 

dp = updater.dispatcher

#creamos los manejadores

dp.add_handler(CommandHandler("start",start))
dp.add_handler(CommandHandler("random",random_number))
dp.add_handler(MessageHandler(Filters.text, echo))

run(updater)


"""PARSE_MODE = "HTML"
<b>bold</b>, <strong>bold</strong>
<i>italic</i>, <em>italic</em>
<u>underline</u>, <ins>underline</ins>
<s>strikethrough</s>, <strike>strikethrough</strike>, <del>strikethrough</del>
<b>bold <i>italic bold <s>italic bold strikethrough</s> <u>underline italic bold</u></i> bold</b>
<a href="http://www.example.com/">inline URL</a>
<a href="tg://user?id=123456789">inline mention of a user</a>
<code>inline fixed-width code</code>
<pre>pre-formatted fixed-width code block</pre>
<pre><code class="language-python">pre-formatted fixed-width code block written in the Python programming language</code></pre>"""