import logging
import os
import telegram
import random
import sys
import urllib.request, json
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import MessageEntity, InlineKeyboardMarkup
from pytube import YouTube, Playlist
import telebot
import requests
import youtube_dl


#configurar loggin

logging.basicConfig(
    level= logging.INFO, format="%(asctime)s-%(name)s-%(levelname)s-%(message)s,"
)
logger = logging.getLogger()

#solicitar token

TOKEN = os.getenv("TOKEN")
mode = os.getenv("MODE")
ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s%(ext)s'})

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
    logger.info(f"El usuario {update.effective_user['first_name']}, ha iniciado una conversacion")
    name = update.effective_user['first_name']
    update.message.reply_text(f"Hola {name} yo soy tu bot.")

def random_number(update,context):
    user_id = update.effective_user['id']
    chat_id = update.effective_chat['id']
    logger.info(f"El {user_id}, ha solicitado un numero aleatorio")
    number = random.randint(0,10)
    context.bot.send_message(chat_id=chat_id, text='<b>bold</b> <i>italic</i> <a href="http://google.com">link</a>.', parse_mode=telegram.ParseMode.HTML)
    #context.bot.sendMessage(chat_id = chat_id, parse_mode="HTML", text=f"<a href="http://www.example.com/">inline URL</a>")
    #context.bot.sendMessage(chat_id = chat_id, parse_mode="HTML", text=f"<b>Numero</b> aleatorio:\n{number}")
    update.message.reply_text(f"Numero aleatorio: {number}")
    

"""def echo(update,context):
    user_id = update.effective_user['id']
    chat_id = update.effective_chat['id']
    logger.info(f"El usuario {user_id}, ha enviado un mensaje de texto")
    text = update.message.text
    context.bot.sendMessage (
        chat_id = chat_id,
        parse_mode = "MarkdownV2",
        text = f"*Escribiste*\n_{text}_"
    )"""

"""def fetchjson(url):
    resp = urllib.request.urlopen(url)
    return json.dumps(resp.read().decode)"""

def buscar(update, context):
    aux = update.message.text
    x = aux.replace("/buscar ", "")
    datos = "search="+x
    print(datos)
    r = requests.post('https://playlist-maker.azurewebsites.net/api/musica2?comando=play',params=datos)
    var1 = r.text
    print(var1)
    user_id = update.effective_user['id']
    #chat_id = update.effective_chat['id']
    logger.info(f"El {user_id}, ha solicitado una busqueda")
    """x = update.message.parse_entities(types=MessageEntity.URL)
    print(x)
    for i in x:
        a = ""+x[i]
        print(type(a))
    thepage = urllib.request.urlopen(a).read().decode('utf-8')"""
    var2 = json.loads(var1)
    print("EL TIPO DE VAR 2 ES: ", type(var2))
    print(var2)
    print(var2[0])
    titulo = var2[0]["title"]
    subtitulo = var2[0]["subtitle"]
    imagen = var2[0]["img"]
    enlace = var2[0]["path"]
    #print("Título => " , var2[0]["title"])
    update.message.reply_text(f"Título: {titulo}")
    update.message.reply_text(f"Subtitulo: {subtitulo}")
    update.message.reply_text(f"Imagen: {imagen}")
    update.message.reply_text(f"Link: {enlace}")
    try:
        with ydl:
            result = ydl.extract_info(
                enlace,
                download=False  # We just want to extract the info
            )

        if 'entries' in result:
            # Can be a playlist or a list of videos
            video = result['entries'][0]
        else:
            # Just a video
            video = result
        
        for i in video['formats']:
            link = '<a href=\"' + i['url'] + '\">' + 'link' + '</a>'

            if i.get('format_note'):
                update.message.reply_text( 'Quality- ' + i['format_note'] + ': ' + link, parse_mode='HTML')
            else:
                update.message.reply_text( link, parse_mode='HTML', disable_notification=True)
    except:
        update.message.reply_text('This can\'t be downloaded by me')
    #context.bot.send_message(chat_id=chat_id, text=f"<b>Numero aleatorio:</b> {titulo}", parse_mode=telegram.ParseMode.HTML)
    #print(var1)
    #resp = urllib.request.urlopen('https://playlistmaker.app.smartmock.io/musica?comando=play&search=tubusqueda')
    #print(resp)
    #thepage = urllib.request.urlopen('https://playlistmaker.app.smartmock.io/musica?comando=play&search=tubusqueda').read().decode('utf-8')
    #print(thepage)
    

"""def hola(update, context):
    name = update.effective_user['first_name']
    if(update.message.text.upper().find("HOLA") >= 0):
        update.message.reply_text(f"Hola {name}")"""


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
dp.add_handler(CommandHandler("buscar",buscar))
#dp.add_handler(MessageHandler(Filters.entity(MessageEntity.URL) ,buscar))
#dp.add_handler(MessageHandler(Filters.text, hola))
#dp.add_handler(MessageHandler(Filters.text, echo))


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