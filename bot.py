import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes, ConversationHandler

# ========== SETTINGS ==========
TOKEN = os.getenv("TOKEN")
CHANNEL_ID = -1003741615712 # ✅ BD BUSSID LOVER চ্যানেল ID
CHANNEL_LINK = "https://t.me/bdbussidlover"
BKASH = "01832533534"
MY_ID = 7304092520 # Nayem ভাই

# 1, 4, 16 = ফ্রি
FREE_MAPS = {
    "map1": ["1. ঢাকা টু রংপুর", "https://drive.google.com/drive/folders/1MqUuSO5n_o5_0WzUeyE3RQen6FXutiRW"],
    "map4": ["4. Bangladesh 300 Fit", "https://drive.google.com/drive/folders/1-jNRfPjI4OlGfDQEglfMuCk2mtj7hedV"],
    "map16": ["16. যমুনা সেতু ম্যাপ", "https://drive.google.com/file/d/123BVMajNDXwXaz7x3Y5woUKY1y4d6GAj/view?usp=drivesdk"]
}

# বাকি 18 টা = 40 টাকা
PAID_MAPS = {
    "p2": ["2. ঢাকা টু চট্টগ্রাম", "https://drive.google.com/drive/folders/169GKO51_Dyg6XEAkLO0hrT2WymW87cbM"],
    "p3": ["3. ঢাকা টু খুলনা টু বরিশাল", "https://drive.google.com/drive/folders/12-IlJJzulZF-B-JAnjK9ZEvLgcrxUxxL"], # ✅ নতুন লিংক বসানো
    "p5": ["5. সুন্দরবন ম্যাপ", "https://drive.google.com/drive/folders/1yq9N7zucXZL4PuGBJLzsSzi3xgE2e7sv"],
    "p6": ["6. চট্টগ্রাম টু কক্সবাজার", "https://drive.google.com/drive/folders/1qB8bMLI7o7r3EibXx0796V5NTU4nM9ZS"],
    "p7": ["7. বগুড়া টু রংপুর", "https://drive.google.com/drive/folders/1GaLRR3ObFJmW8dNERf-qfuRw5z9e2YX_"],
    "p8": ["8. জামালপুর টু ময়মনসিংহ", "https://drive.google.com/drive/folders/1XEsR343OtyBn4nVvbaYPOo6XVKl1UVX6"],
    "p9": ["9. টাঙ্গাইল টু সিরাজগঞ্জ", "https://drive.google.com/drive/folders/1_XNiE-8r3XMyuJN3T9iD0v41tmBX1HLI"], # যমুনা 2.0
    "p10": ["10. অষ্টগ্ৰাম হাওর ম্যাপ", "https://drive.google.com/drive/folders/1mNHEmcKJnO6hr7Wjcd7xcQ3Zmte8UlnF"],
    "p11": ["11. বাংলাদেশ ভাটিয়া রেলস্টেশন ম্যাপ+ ট্রেন মোড", "https://drive.google.com/drive/folders/13J85P8ZRDPuS-KyJrnszQfUnr-IVQVE1"],
    "p12": ["12. মধুমতি সেতু ম্যাপ", "https://drive.google.com/drive/folders/1edUHkKWxifFQsG_oluGXTjJGw2hNj1TN"],
    "p13": ["13. কুয়াকাটা টু কলাপাড়া", "https://drive.google.com/drive/folders/1ae5Qu3i2WXjMEzt9_DSK-p4eB7a3i8un"],
    "p14": ["14. গড়াই সেতু ম্যাপ মোড", "https://drive.google.com/drive/folders/1P77jKBlxGlAoPxKD2-VVnJNwpV1vfc7o"],
    "p15": ["15. রাজশাহী টু বরিশাল", "https://drive.google.com/drive/folders/1FheeZ49p62z4YWxWKSU22R_2RjC4iALg"],
    "p17": ["17. বান্দরবান টু খাগড়াছড়ি", "https://drive.google.com/drive/folders/1uEkN7wwXE5C_NPfYTD73xYRGJ_aiBfMb"],
    "p18": ["18. ঢাকা টু সিলেট ম্যাপ", "https://drive.google.com/drive/folders/1GUeCsyvH16JW5UcZ164KU0G_exjb4RiE"],
    "p19": ["19. বাংলাদেশী গ্ৰাম ম্যাপ", "https://drive.google.com/drive/folders/1aXHSa9p-EIfseY1UOeNRCL5riKx3KkhP"],
    "p20": ["20. বরিশাল টু খুলনা ম্যাপ", "DRIVE_LINK_20"], # ⚠️ লিংক বাকি
    "p21": ["21. ঢাকা মাওয়া হাইওয়ে", "https://drive.google.com/drive/folders/1mnRyQCrAFL2pHQI6dShc1lALkta5bOi5"],
}

WAITING_SCREENSHOT = 1
user_data = {}

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

async def check_channel_member(user_id, context):
    try:
        member = await context.bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        return member.status in ['member', 'administrator', 'creator']
    except:
        return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🆓 ফ্রি ম্যাপ ৩টি", callback_data='free')],
        [InlineKeyboardButton("💎 পেইড ম্যাপ 18টি - 40 টাকা", callback_data='paid')]
    ]
    await update.message.reply_text("🚌 **BD Bussid Map Bot**\n\nনিচ থেকে ম্যাপ সিলেক্ট করো:", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == 'free':
        keyboard = [[InlineKeyboardButton(name[0], callback_data=key)] for key, name in FREE_MAPS.items()]
        await query.edit_message_text("🆓 নিচ থেকে ১টি ফ্রি ম্যাপ নাও:", reply_markup=InlineKeyboardMarkup(keyboard))
    elif query.data == 'paid':
        keyboard = [[InlineKeyboardButton(f"{name[0]} - 40৳", callback_data=key)] for key, name in PAID_MAPS.items()]
        await query.edit_message_text("💎 নিচ থেকে ১টি পেইড ম্যাপ সিলেক্ট করো:", reply_markup=InlineKeyboardMarkup(keyboard))

async def map_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    data = query.data

    if data in FREE_MAPS:
        if await check_channel_member(user_id, context):
            name, link = FREE_MAPS[data]
            await query.edit_message_text(f"✅ **{name}**\n\nডাউনলোড লিংক: `{link}`", parse_mode='Markdown')
        else:
            await query.edit_message_text(f"⚠️ ফ্রি ম্যাপ নিতে আগে চ্যানেলে জয়েন করতে হবে।\n\n👉 {CHANNEL_LINK}\n\nজয়েন করে আবার ম্যাপে ক্লিক করো।")

    elif data in PAID_MAPS:
        user_data[user_id] = data
        name, link = PAID_MAPS[data]
        if "DRIVE_LINK" in link:
            await query.edit_message_text("⚠️ এই ম্যাপের লিংক এখনো এড করা হয়নি। পরে আবার চেষ্টা করুন।")
            return ConversationHandler.END
        text = f"💰 **{name}**\n\nপেমেন্ট: **40 টাকা**\nবিকাশ/নগদ/রকেট: `{BKASH}`\n\nটাকা পাঠিয়ে স্কিনশট এই চ্যাটে পাঠাও।"
        await query.edit_message_text(text, parse_mode='Markdown')
        return WAITING_SCREENSHOT

async def screenshot_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id in user_data:
        map_key = user_data[user_id]
        map_name = PAID_MAPS[map_key][0]
        await context.bot.forward_message(chat_id=MY_ID, from_chat_id=update.message.chat_id, message_id=update.message_id)
        keyboard = [[InlineKeyboardButton("✅ Approve & Send", callback_data=f"approve_{user_id}_{map_key}")]]
        await context.bot.send_message(chat_id=MY_ID, text=f"🔔 নতুন অর্ডার!\nUser: @{update.message.from_user.username}\nUser ID: `{user_id}`\nMap: {map_name}", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')
        await update.message.reply_text(f"✅ স্কিনশট পেয়েছি। `{map_name}` চেক করে ৫ মিনিটের মধ্যে লিংক দিয়ে দিবো।", parse_mode='Markdown')
        del user_data[user_id]
    return ConversationHandler.END

async def approve_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    _, user_id, map_key = query.data.split('_')
    user_id = int(user_id)
    name, link = PAID_MAPS[map_key]
    await context.bot.send_message(chat_id=user_id, text=f"✅ পেমেন্ট Approved!\n\n**{name}**\nডাউনলোড লিংক: `{link}`", parse_mode='Markdown')
    await query.edit_message_text("✅ লিংক পাঠানো হয়েছে।")

def main():
    app = Application.builder().token(TOKEN).build()
    conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(map_handler, pattern='^(map|p)')],
        states={WAITING_SCREENSHOT: [MessageHandler(filters.PHOTO, screenshot_handler)]},
        fallbacks=[]
    )
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(menu_handler, pattern='^(free|paid)$'))
    app.add_handler(CallbackQueryHandler(approve_handler, pattern='^approve_'))
    app.add_handler(conv)
    print("BD Bussid Map Bot Running...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
