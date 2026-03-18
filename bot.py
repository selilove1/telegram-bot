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
ADMIN_ID = 7865928520
GROUP_ID = -1003750352591
recent_buyers = []
QR_IMAGE = "https://ik.imagekit.io/q3emnf9bso/photo_6183553850615205462_y.jpg"
MAIN_IMAGE = "https://ik.imagekit.io/q3emnf9bso/photo_6183958372109979356_y.jpg"

DEMO_LINK = "https://t.me/itsmy8246"
PROOF_LINK = "https://t.me/proofs8246"
PRIVATE_GROUP = "https://t.me/your_private_group"


# 🔥 START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
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

    # LANGUAGE SELECT
    if data == "hi" or data == "en":

        keyboard = [
            [InlineKeyboardButton("💎 Premium खरीदें", callback_data="buy")],
            [InlineKeyboardButton("🎬 Demo देखें", url=DEMO_LINK)],
            [InlineKeyboardButton("📸 Payment Proofs", url=PROOF_LINK)]
        ]

        await query.message.reply_photo(
            photo=MAIN_IMAGE,
            caption="""
🔥 PREMIUM VIDEO PACK

✔ 50K+ Videos
✔ Instant Access
✔ Lifetime Content

👇 नीचे से option select करें
""",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # BUY
    elif data == "buy":

        keyboard = [
            [InlineKeyboardButton("✅ I PAID", callback_data="paid")]
        ]

        await query.message.reply_photo(
            photo=QR_IMAGE,
            caption="""
💳 PAYMENT DETAILS

Amount: ₹49  
Videos: 50K+

Please Send Exact Amount
""",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # PAID
    elif data == "paid":

        await query.message.reply_text(
            "📸 Payment screenshot भेजो verification के लिए"
        )


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


# 🔥 ADMIN APPROVE
async def admin_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    data = query.data

    if data.startswith("approve_"):

        user_id = int(data.replace("approve_", ""))

        try:
            await context.bot.send_message(
                chat_id=user_id,
                text=f"""
🎉 Payment Approved Successfully!

🔓 Your Access is Ready

👉 Join Private Group:
https://t.me/+xrMXzNKdNzMzYTc1

📌 Important Instructions:
* Daily new videos update होंगे
* Link किसी को share मत करना
* Lifetime access है

🚀 Enjoy your content
"""
            )

            await query.message.reply_text("✅ Approved & Sent")

        except Exception as e:
            await query.message.reply_text(f"❌ Error: {e}")

# 🔥 FAKE PURCHASE
async def fake_notifications(app):

    names = ["Rohit", "Vikas", "Manish", "Sundar", "Karan", "Aakib"]

    while True:

        try:
            # REAL + FAKE mix
            if recent_buyers:
                name = recent_buyers.pop(0)   # REAL USER 🔥
            else:
                name = random.choice(names)   # FAKE USER

            await app.bot.send_message(
                chat_id=GROUP_ID,
                text=f"💸 {name} just purchased Premium!"
            )

        except Exception as e:
            print("ERROR:", e)

        await asyncio.sleep(120)


# 🔥 LIVE COUNTER
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


# 🔥 START TASKS
async def on_start(app):
    print("Bot Running...")
    asyncio.create_task(fake_notifications(app))
    asyncio.create_task(live_counter(app))


# 🔥 MAIN
def main():

    app = ApplicationBuilder().token(TOKEN).post_init(on_start).build()

    # START
    app.add_handler(CommandHandler("start", start))

    # ✅ ADMIN APPROVE (पहले होना चाहिए)
    app.add_handler(CallbackQueryHandler(admin_buttons, pattern="^approve_"))

    # ✅ NORMAL BUTTONS
    app.add_handler(CallbackQueryHandler(button))

    # 📸 SCREENSHOT HANDLER
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    print("Bot Running...")

    app.run_polling()


if __name__ == "__main__":
    main()
