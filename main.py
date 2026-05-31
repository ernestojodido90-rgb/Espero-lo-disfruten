import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters

TOKEN = '8294425780:AAFsJneyGPeLo35arLH2Hv5oaBeCy9iOxDw'
DB_FILE = 'musica.json'

def cargar_db():
    try:
        with open(DB_FILE, 'r') as f: return json.load(f)
    except: return {}

def guardar_db(data):
    with open(DB_FILE, 'w') as f: json.dump(data, f)

async def manejar_audio(update, context):
    if update.message.audio:
        db = cargar_db()
        nombre = update.message.audio.title or update.message.audio.file_name
        db[nombre] = update.message.audio.file_id
        guardar_db(db)
        await update.message.reply_text(f"✅ Guardado: {nombre}")

async def start(update, context):
    db = cargar_db()
    if not db:
        await update.message.reply_text("Envíame música para empezar.")
        return
    keyboard = [[InlineKeyboardButton(nombre, callback_data=nombre)] for nombre in db.keys()]
    await update.message.reply_text("🎵 Elige tu música:", reply_markup=InlineKeyboardMarkup(keyboard))

async def button(update, context):
    query = update.callback_query
    await query.answer()
    db = cargar_db()
    if query.data in db:
        await query.message.reply_audio(audio=db[query.data])

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.AUDIO, manejar_audio))
    app.add_handler(CallbackQueryHandler(button))
    app.run_polling()
