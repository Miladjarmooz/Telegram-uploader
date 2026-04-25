import os
import requests
import re
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import os as os_module

BOT_TOKEN = os.environ.get("BOT_TOKEN")

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
            link = match.group(0)
            await message.reply_text(f"لینک شما:\n{link}")
        else:
            await message.reply_text("لینک پیدا نشد یا آپلود ناموفق بود")

    except Exception as e:
        await message.reply_text(f"خطا: {str(e)}")

    finally:
        if os_module.path.exists(file_path):
            os_module.remove(file_path)


app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.ALL, handle_file))

print("Bot is running...")
app.run_polling()
