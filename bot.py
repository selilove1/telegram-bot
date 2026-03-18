import random
import asyncio
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters
)

# 🔧 CONFIG
TOKEN = "8611185133:AAGrVi6sRaTpGYk47qGO_Ghzf-8hxIrbi_k"
ADMIN_ID = 123456789
GROUP_ID = -1001234567890

QR_IMAGE = "https://your-qr-image-link.com/qr.png"
DEMO_LINK = "https://t.me/your_demo_channel"
PROOF_LINK = "https://t.me/your_proof_channel"
PRIVATE_GROUP = "https://t.me/your_private_group"


# 🔥 START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(str(update.effective_chat.id))
    keyboard = [
        [InlineKeyboardButton("🇮🇳 Hindi", callback_data="hi")],
        [InlineKeyboardButton("🇬🇧 English", callback_data="en")]
    ]

    await update.message.reply_text(
        "🌍 Select Language",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# 🔥 BUTTON HANDLER
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()
    data = query.data

    if data in ["hi", "en"]:

        keyboard = [
            [InlineKeyboardButton("💎 Premium खरीदें", callback_data="buy")],
            [InlineKeyboardButton("🎬 Demo देखें", url=DEMO_LINK)],
            [InlineKeyboardButton("📸 Payment Proofs", url=PROOF_LINK)]
        ]

        await query.message.reply_photo(
            photo=QR_IMAGE,
            caption="🔥 Premium Videos Available\n👇 Choose Option",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif data == "buy":

        keyboard = [
            [InlineKeyboardButton("✅ I PAID", callback_data="paid")]
        ]

        await query.message.reply_photo(
            photo=QR_IMAGE,
            caption="💳 Pay ₹49\nAfter payment click I PAID",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif data == "paid":

        await query.message.reply_text("📸 Send your payment screenshot now")


# 🔥 SCREENSHOT HANDLER
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.message.from_user

    await update.message.reply_text("⏳ Waiting for admin approval")

    keyboard = [
        [InlineKeyboardButton("✅ APPROVE", callback_data=f"approve_{user.id}")]
    ]

    await context.bot.send_photo(
        chat_id=ADMIN_ID,
        photo=update.message.photo[-1].file_id,
        caption=f"💰 Payment from {user.first_name}\nUser ID: {user.id}",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# 🔥 ADMIN APPROVE BUTTON
async def admin_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    data = query.data

    if data.startswith("approve_"):

        user_id = int(data.split("_")[1])

        await context.bot.send_message(
            chat_id=user_id,
            text=f"🎉 Payment Approved!\n\n👉 Join here:\n{PRIVATE_GROUP}"
        )

        await query.message.reply_text("✅ Approved Successfully")


# 🔥 FAKE PURCHASE NOTIFICATIONS
async def fake_notifications(app):

    names = ["Rahul", "Aman", "Rohit", "Vikas", "Suresh", "Neha", "Pooja"]

    while True:

        name = random.choice(names)

        try:
            await app.bot.send_message(
                chat_id=GROUP_ID,
                text=f"⚡ {name} just purchased Premium Pack"
            )
        except:
            pass

        await asyncio.sleep(120)


# 🔥 LIVE COUNTER (NEW ADD)
async def live_counter(app):

    while True:

        count = random.randint(120, 350)

        try:
            await app.bot.send_message(
                chat_id=GROUP_ID,
                text=f"🔥 {count}+ users are viewing right now!"
            )
        except:
            pass

        await asyncio.sleep(90)


# 🔥 ON START
async def on_start(app):
    print("Bot Running...")
    asyncio.create_task(fake_notifications(app))
    asyncio.create_task(live_counter(app))  # 👈 added


# 🔥 MAIN
def main():

    app = ApplicationBuilder().token(TOKEN).post_init(on_start).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(CallbackQueryHandler(admin_buttons, pattern="approve_"))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    print("Bot Running...")

    app.run_polling()


if __name__ == "__main__":
    main()
