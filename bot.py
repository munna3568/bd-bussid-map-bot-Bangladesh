import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

TOKEN = os.getenv("BOT_TOKEN")

FREE_MAPS = [
    "🚌 ঢাকা টু রংপুর",
    "🚌 Bangladesh 300 Fit",
    "🚌 যমুনা সেতু ম্যাপ"
]

PREMIUM_MAPS = [
    "💎 ঢাকা টু চট্টগ্রাম",
    "💎 ঢাকা টু খুলনা টু বরিশাল",
    "💎 সুন্দরবন ম্যাপ",
    "💎 চট্টগ্রাম টু কক্সবাজার",
    "💎 বগুড়া টু রংপুর",
    "💎 জামালপুর টু ময়মনসিংহ",
    "💎 যমুনা সেতু ২.০",
    "💎 অষ্টগ্রাম হাওর ম্যাপ",
    "💎 বাংলাদেশ ভাটিয়া রেলস্টেশন + ট্রেন মোড",
    "💎 মধুমতি সেতু ম্যাপ",
    "💎 কুয়াকাটা টু কলাপাড়া",
    "💎 গড়াই সেতু ম্যাপ",
    "💎 রাজশাহী টু বরিশাল",
    "💎 বান্দরবান ম্যাপ",
    "💎 ঢাকা টু সিলেট (নতুন)",
    "💎 বাংলাদেশী গ্রাম ম্যাপ",
    "💎 বরিশাল টু খুলনা (নতুন)",
    "💎 ঢাকা মাওয়া হাইওয়ে"
]

PAYMENT = """
💳 প্রতি Premium Map এর মূল্য: ৪০ টাকা
📱 bKash / Nagad / Rocket
01832533534

পেমেন্ট করার পর Transaction ID অথবা Screenshot পাঠান।
👤 Admin: @Nayem802325
"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🆓 Free Maps", callback_data="free")],
        [InlineKeyboardButton("💎 Premium Maps", callback_data="premium")],
        [InlineKeyboardButton("💳 Payment", callback_data="payment")],
        [InlineKeyboardButton("📞 Contact Admin", url="https://t.me/Nayem802325")]
    ]
    await update.message.reply_text(
        "🇧🇩 Welcome to BD BUSSID MAP BOT Bangladesh\nনিচের অপশন নির্বাচন করুন 👇",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "free":
        text = "🆓 FREE MAPS\n\n"
        for i, m in enumerate(FREE_MAPS, start=1):
            text += f"{i}. {m}\n"
        text += "\n📥 ফ্রি ম্যাপ পেতে Admin এর সাথে যোগাযোগ করুন।"
        keyboard = [
            [InlineKeyboardButton("📞 Contact Admin", url="https://t.me/Nayem802325")],
            [InlineKeyboardButton("⬅️ Back", callback_data="home")]
        ]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == "premium":
        text = "💎 PREMIUM MAPS\n\n"
        for i, m in enumerate(PREMIUM_MAPS, start=1):
            text += f"{i}. {m}\n"
        text += "\n💰 প্রতি ম্যাপের মূল্য: ৪০ টাকা\n\n👤 কিনতে যোগাযোগ করুন:\n@Nayem802325"
        keyboard = [
            [InlineKeyboardButton("💳 Payment", callback_data="payment")],
            [InlineKeyboardButton("📞 Contact Admin", url="https://t.me/Nayem802325")],
            [InlineKeyboardButton("⬅️ Back", callback_data="home")]
        ]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == "payment":
        keyboard = [
            [InlineKeyboardButton("📞 Send Screenshot", url="https://t.me/Nayem802325")],
            [InlineKeyboardButton("⬅️ Back", callback_data="home")]
        ]
        await query.edit_message_text(PAYMENT, reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == "home":
        keyboard = [
            [InlineKeyboardButton("🆓 Free Maps", callback_data="free")],
            [InlineKeyboardButton("💎 Premium Maps", callback_data="premium")],
            [InlineKeyboardButton("💳 Payment", callback_data="payment")],
            [InlineKeyboardButton("📞 Contact Admin", url="https://t.me/Nayem802325")]
        ]
        await query.edit_message_text(
            "🇧🇩 Welcome to BD BUSSID MAP BOT Bangladesh\nনিচের অপশন নির্বাচন করুন 👇",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

def main():
    if not TOKEN:
        raise ValueError("BOT_TOKEN পাওয়া যায়নি। Railway → Variables-এ BOT_TOKEN সেট করুন।")
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    print("🇧🇩 BD BUSSID MAP BOT Bangladesh Running...")
    app.run_polling()  # এখানে ঠিক করে দিছি

if __name__ == "__main__":
    main()
