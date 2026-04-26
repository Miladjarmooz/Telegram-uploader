import os
import requests
import re
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")


async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message

    file = None
    file_name = "file"

    if message.document:
        file = message.document
        file_name = file.file_name
    elif message.photo:
        file = message.photo[-1]
        file_name = "photo.jpg"
    elif message.video:
        file = message.video
        file_name = "video.mp4"
    else:
        await message.reply_text("فایل پشتیبانی نمی‌شود")
        return

    tg_file = await file.get_file()
    file_path = f"./{file_name}"
    await tg_file.download_to_drive(file_path)

    await message.reply_text("در حال آپلود...")

    try:
        with open(file_path, "rb") as f:
            response = requests.post(
                "https://www.uploadb.com/upload",
                files={"file": (file_name, f)}
            )

        match = re.search(r"https://www\.uploadb\.com/\w+", response.text)
        if match:
            await message.reply_text(f"لینک:\n{match.group(0)}")
        else:
            await message.reply_text("آپلود ناموفق بود")

    except Exception as e:
        await message.reply_text(f"خطا: {e}")


app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(MessageHandler(filters.ALL, handle_file))

print("Bot is running...")
app.run_polling()
