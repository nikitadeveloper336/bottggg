import json
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

with open("songs.json", "r", encoding="utf-8") as f:
    songs = json.load(f)

user_data = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Готов к музыкальной викторине? Напиши /quiz")

async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    song = random.choice(songs)
    user_data[update.effective_user.id] = song

    keyboard = [[InlineKeyboardButton(opt, callback_data=opt)] for opt in song["options"]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    with open(song["file"], "rb") as voice:
        await update.message.reply_voice(voice)

    await update.message.reply_text("Что это за песня?", reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    song = user_data.get(user_id)
    
    if not song:
        await query.edit_message_text("Сначала начни с /quiz")
        return

    if query.data == song["answer"]:
        await query.edit_message_text("Правильно!")
    else:
        await query.edit_message_text(f"Неправильно! Правильный ответ: {song['answer']}")

app = ApplicationBuilder().token("7590308951:AAGDpqfTiNjxKL5oK3EPI9lXEVFtPD6_MrQ").build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("quiz", quiz))
app.add_handler(CallbackQueryHandler(button))

import os

PORT = int(os.environ.get('PORT', 8443))
WEBHOOK_URL = os.environ.get('WEBHOOK_URL')  # ты задашь это в Render

app.run_webhook(
    listen="0.0.0.0",
    port=PORT,
    webhook_url=WEBHOOK_URL
)
