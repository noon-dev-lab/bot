from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters


# Token dari BotFather
TOKEN = "8019702056:AAGvp-2_wKrNY7h2-MeCDl1XQ6z7AS-nXeo"

# Path ke file foto
PHOTO_FILE = "tutor.jpg"

# Inisialisasi variabel untuk menyimpan data
user_data = {}


# Perintah /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_data[user_id] = {"link_message": None, "verified": False}

    # Cetak di terminal
    print(f"[START] User ID: {user_id} memulai bot")

    # Kirim foto tutor ke pengguna
    with open(PHOTO_FILE, "rb") as photo:
        await update.message.reply_photo(photo)

    # Kirim panduan setelah mengirim file foto
    await update.message.reply_text(
        "Selamat datang! Silakan ikuti panduan berikut:\n"
        "1. Kirim link pesan dengan format /sendvideo.\n"
        "2. Setelah mengirim link, ikuti panduan untuk verifikasi lebih lanjut."
    )


# Perintah /sendvideo
async def send_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_data[user_id]["link_message"] = None  # Reset data sebelumnya
    await update.message.reply_text(
        "Silakan kirimkan link pesan yang ingin Anda gunakan untuk verifikasi."
    )
    print(f"[SEND VIDEO] User ID: {user_id} meminta untuk mengirim link pesan.")


# Handler untuk menerima pesan link dari pengguna
async def receive_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_data.get(user_id):
        user_data[user_id]["link_message"] = update.message.text
        print(f"[LINK MESSAGE] User ID: {user_id} - Link pesan diterima: {update.message.text}")

        await update.message.reply_text(
            "Link pesan telah diterima. Sekarang silakan kirim kode verifikasi dari telegram untuk melanjutkan."
        )
    else:
        await update.message.reply_text(
            "Silakan gunakan perintah /start terlebih dahulu untuk memulai alur ini."
        )


# Handler untuk menerima verifikasi
async def verify(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_data.get(user_id) and user_data[user_id]["link_message"]:
        user_data[user_id]["verified"] = True
        print(f"[VERIFY] User ID: {user_id} berhasil memverifikasi dengan link: {user_data[user_id]['link_message']}")

        await update.message.reply_text(
            "Verifikasi berhasil! Proses selanjutnya akan dilakukan sesuai dengan permintaan Anda."
        )
    else:
        await update.message.reply_text(
            "Silakan kirim link pesan terlebih dahulu menggunakan perintah /sendvideo."
        )


# Fungsi utama untuk menjalankan bot
def main():
    # Buat Application dengan token bot
    application = Application.builder().token(TOKEN).build()

    # Tambahkan handler
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("sendvideo", send_video))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, receive_link))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, verify))

    # Jalankan bot
    print("[BOT STARTED] Bot is running...")
    application.run_polling()


if __name__ == "__main__":
    main()
