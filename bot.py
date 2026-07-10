import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes, ConversationHandler

TOKEN = os.getenv("TOKEN")
CHANNEL_ID = -1003741615712
CHANNEL_USERNAME = "@bdbussidlover" 
CHANNEL_URL = "https://t.me/bdbussidlover"
BKASH = "01832533534"
MY_ID = 7304092520

FREE_MAPS = {
    "map1": ["1. ঢাকা টু রংপুর", "https://drive.google.com/drive/folders/1MqUuSO5n_o5_0WzUeyE3RQen6FXutiRW"],
    "map4": ["4. Bangladesh 300 Fit", "https://drive.google.com/drive/folders/1-jNRfPjI4OlGfDQEglfMuCk2mtj7hedV"],
    "map16": ["16. যমুনা সেতু ম্যাপ", "https://drive.google.com/file/d/123BVMajNDXwXaz7x3Y5woUKY1y4d6GAj/view?usp=drivesdk"]
}

PAID_MAPS = {
    "p2": ["2. ঢাকা টু চট্টগ্রাম", "https://drive.google.com/drive/folders/169GKO51_Dyg6XEAkLO0hrT2WymW87cbM"],
    #... বাকি সব PAID_MAPS
    "p21": ["21. ঢাকা মাওয়া হাইওয়ে", "https://drive.google.com/drive/folders/1mnRyQCrAFL2pHQI6dShc1lALkta5bOi5"],
}

WAITING_SCREENSHOT = 1
user_data = {}
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

async def check_channel_member(user_id, context):
    try:
        member = await context.bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        return member.status in ['member', 'administrator', 'creator']
    except Exception as e:
        logging.error(f"Channel check error: {e}")
        return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🆓 ফ্রি ম্যাপ ৩টি", callback_data='free')],
        [InlineKeyboardButton("💎 পেইড ম্যাপ 18টি - 40 টাকা", callback_data='paid')]
    ]
    footer = f"\n\n💳 পেমেন্ট: `{BKASH}`\n📢 চ্যানেল: {CHANNEL_USERNAME}"
    text = "🚌 **BD Bussid Map Bot**\n\nনিচ থেকে ম্যাপ সিলেক্ট করো:" + footer
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown', disable_web_page_preview=True)

async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query; await query.answer()
    footer = f"\n\n💳 পেমেন্ট: `{BKASH}`\n📢 চ্যানেল: {CHANNEL_USERNAME}"
    if query.data == 'free':
        keyboard = [[InlineKeyboardButton(name[0], callback_data=key)] for key, name in FREE_MAPS.items()]
        text = "🆓 নিচ থেকে ১টি ফ্রি ম্যাপ নাও:" + footer
        await query.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown', disable_web_page_preview=True) # edit এর বদলে reply
    elif query.data == 'paid':
        keyboard = [[InlineKeyboardButton(f"{name[0]} - 40৳", callback_data=key)] for key, name in PAID_MAPS.items()]
        text = "💎 নিচ থেকে ১টি পেইড ম্যাপ সিলেক্ট করো:" + footer
        await query.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown', disable_web_page_preview=True) # edit এর বদলে reply

async def map_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query; await query.answer(); user_id = query.from_user.id; data = query.data
    footer = f"\n\n💳 পেমেন্ট: `{BKASH}`\n📢 চ্যানেল: {CHANNEL_USERNAME}"
    
    if data in FREE_MAPS:
        if await check_channel_member(user_id, context):
            name, link = FREE_MAPS[data]; text = f"✅ **{name}**\n\nডাউনলোড লিংক: `{link}`" + footer
            await query.message.reply_text(text, parse_mode='Markdown', disable_web_page_preview=True) # নতুন মেসেজ
        else:
            keyboard = [[InlineKeyboardButton("🔄 আবার চেক করুন", callback_data=data)]]
            text = f"⚠️ ফ্রি ম্যাপ নিতে আগে চ্যানেলে জয়েন করতে হবে।\n\n👉 {CHANNEL_URL}\n\nজয়েন করে নিচের বাটনে চাপো।"
            await query.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), disable_web_page_preview=True)
            
    elif data in PAID_MAPS:
        user_data[user_id] = data; name, link = PAID_MAPS[data]
        if "DRIVE_LINK" in link:
            await query.message.reply_text("⚠️ এই ম্যাপের লিংক এখনো এড করা হয়নি।"); return ConversationHandler.END
        text = f"💰 **{name}**\n\nপেমেন্ট: **40 টাকা**\nবিকাশ/নগদ/রকেট: `{BKASH}`\n\nটাকা পাঠিয়ে স্কিনশট এই চ্যাটে পাঠাও।" + footer
        await query.message.reply_text(text, parse_mode='Markdown', disable_web_page_preview=True) # নতুন মেসেজ
        return WAITING_SCREENSHOT

async def screenshot_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id in user_data:
        map_key = user_data[user_id]; map_name = PAID_MAPS[map_key][0]
        await context.bot.forward_message(chat_id=MY_ID, from_chat_id=update.message.chat_id, message_id=update.message_id)
        keyboard = [[InlineKeyboardButton("✅ Approve & Send", callback_data=f"approve_{user_id}_{map_key}")]]
        await context.bot.send_message(chat_id=MY_ID, text=f"🔔 নতুন অর্ডার!\nUser: @{update.message.from_user.username}\nUser ID: `{user_id}`\nMap: {map_name}", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')
        await update.message.reply_text(f"✅ স্কিনশট পেয়েছি। `{map_name}` চেক করে ৫ মিনিটের মধ্যে লিংক দিয়ে দিবো।", parse_mode='Markdown'); del user_data[user_id]
    return ConversationHandler.END

async def approve_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query; await query.answer(); _, user_id, map_key = query.data.split('_'); user_id = int(user_id)
    name, link = PAID_MAPS[map_key]
    footer = f"\n\n💳 পেমেন্ট: `{BKASH}`\n📢 চ্যানেল: {CHANNEL_USERNAME}"
    await context.bot.send_message(chat_id=user_id, text=f"✅ পেমেন্ট Approved!\n\n**{name}**\nডাউনলোড লিংক: `{link}`" + footer, parse_mode='Markdown', disable_web_page_preview=True)
    await query.edit_message_text("✅ লিংক পাঠানো হয়েছে।")

def main():
    app = Application.builder().token(TOKEN).build()
    conv = ConversationHandler(entry_points=[CallbackQueryHandler(map_handler, pattern='^(map|p)')], states={WAITING_SCREENSHOT: [MessageHandler(filters.PHOTO, screenshot_handler)]}, fallbacks=[])
    app.add_handler(CommandHandler("start", start)); app.add_handler(CallbackQueryHandler(menu_handler, pattern='^(free|paid)$'))
    app.add_handler(CallbackQueryHandler(approve_handler, pattern='^approve_')); app.add_handler(conv)
    print("BD Bussid Map Bot Running v2.2...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
