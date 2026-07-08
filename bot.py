import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

FREE_MAPS = [
    "🚌 ঢাকা টু রংপুর",
    "🚌 Bangladesh 300 Fit",
    "🚌 যমুনা সেতু ম্যাপ",
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
]

PAYMENT = """
💳 Premium Map মূল্য: ৪০ টাকা

📱 bKash / Nagad / Rocket
01832533534

পেমেন্ট করার পর Screenshot অথবা Transaction ID পাঠান।

👤 Admin:
@Nayem802325
"""


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🆓 Free Maps", callback_data="free")],
        [InlineKeyboardButton("💎 Premium Maps", callback_data="premium")],
        [InlineKeyboardButton("💳 Payment", callback_data="payment")],
        [InlineKeyboardButton("📞 Contact Admin", url="https://t.me/Nayem802325")],
    ]

    await update.message.reply_text(
        "🇧🇩 BD BUSSID MAP BOT Bangladesh\n\nনিচের অপশন নির্বাচন করুন 👇",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "free":
        text = "🆓 FREE MAPS\n\n"
        for i, m in enumerate(FREE_MAPS, 1):
            text += f"{i}. {m}\n"

        await query.edit_message_text(
            text,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("⬅️ Back", callback_data="home")]]
            ),
        )

    elif query.data == "premium":
        text = "💎 PREMIUM MAPS\n\n"
        for i, m in enumerate(PREMIUM_MAPS, 1):
            text += f"{i}. {m}\n"

        await query.edit_message_text(
            text,
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("💳 Payment", callback_data="payment")],
                    [InlineKeyboardButton("⬅️ Back", callback_data="home")],
                ]
            ),
        )

    elif query.data == "payment":
        await query.edit_message_text(
            PAYMENT,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("⬅️ Back", callback_data="home")]]
            ),
        )

    elif query.data == "home":
        keyboard = [
            [InlineKeyboardButton("🆓 Free Maps", callback_data="free")],
            [InlineKeyboardButton("💎 Premium Maps", callback_data="premium")],
            [InlineKeyboardButton("💳 Payment", callback_data="payment")],
            [InlineKeyboardButton("📞 Contact Admin", url="https://t.me/Nayem802325")],
        ]

        await query.edit_message_text(
            "🇧🇩 BD BUSSID MAP BOT Bangladesh\n\nনিচের অপশন নির্বাচন করুন 👇",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )


def main():
    token = os.getenv("BOT_TOKEN")

    if not token:
        raise ValueError("BOT_TOKEN পাওয়া যায়নি!")

    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))

    print("Bot Running...")
    app.run_polling()


if __name__ == "__main__":
    main()
