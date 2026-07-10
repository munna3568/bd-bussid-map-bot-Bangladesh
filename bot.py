import os
import logging
import uuid
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("TOKEN")
CHANNEL_ID = -1003741615712 # @bdbussidlover
FREE_CHANNEL_ID = -1004392467475 # BD ETS2 LOVER ANDROID - নতুন ID বসানো হলো
CHANNEL_USERNAME = "@bdbussidlover"
FREE_CHANNEL_URL = "https://t.me/bdets2loverandroid" # চ্যানেলের ইউজারনেম থাকলে এটা দাও। না থাকলে t.me/c/1004392467475
CHANNEL_URL = "https://t.me/bdbussidlover"
YOUTUBE_URL = "https://www.youtube.com/@NHMMunna"
FB_URL = "https://www.facebook.com/profile.php?id=61587406053752"
BKASH = "01832533534"
MY_ID = 7304092520

FREE_MAPS = {
    "map1": ["1. ঢাকা টু রংপুর", "https://drive.google.com/drive/folders/1MqUuSO5n_o5_0WzUeyE3RQen6FXutiRW"],
    "map2": ["2. Bangladesh 300 Fit", "https://drive.google.com/drive/folders/1-jNRfPjI4OlGfDQEglfMuCk2mtj7hedV"],
    "map3": ["3. যমুনা সেতু ম্যাপ", "https://drive.google.com/file/d/123BVMajNDXwXaz7x3Y5woUKY1y4d6GAj/view?usp=drivesdk"],
    "map4": ["4. রাজশাহী টু বরিশাল", "https://drive.google.com/drive/folders/1FheeZ49p62z4YWxWKSU22R_2RjC4iALg"], # ফ্রি
}

PAID_MAPS = {
    "p5": ["5. ঢাকা টু চট্টগ্রাম", "https://drive.google.com/drive/folders/169GKO51_Dyg6XEAkLO0hrT2WymW87cbM"],
    "p6": ["6. ঢাকা টু খুলনা টু বরিশাল ভায়া", "https://drive.google.com/drive/folders/12-IlJJzulZF-B-JAnjK9ZEvLgcrxUxxL"],
    "p7": ["7. সুন্দরবন ম্যাপ", "https://drive.google.com/drive/folders/1yq9N7zucXZL4PuGBJLzsSzi3xgE2e7sv"],
    "p8": ["8. চট্টগ্রাম টু কক্সবাজার", "https://drive.google.com/drive/folders/1qB8bMLI7o7r3EibXx0796V5NTU4nM9ZS"],
    "p9": ["9. বগুড়া টু রংপুর", "https://drive.google.com/drive/folders/1GaLRR3ObFJmW8dNERf-qfuRw5z9e2YX_"],
    "p10": ["10. জামালপুর টু ময়মনসিংহ", "https://drive.google.com/drive/folders/1XEsR343OtyBn4nVvbaYPOo6XVKl1UVX6"],
    "p11": ["11. টাঙ্গাইল টু সিরাজগঞ্জ", "https://drive.google.com/drive/folders/1_XNiE-8r3XMyuJN3T9iD0v41tmBX1HLI"],
    "p12": ["12. অষ্টগ্ৰাম হাওর ম্যাপ", "https://drive.google.com/drive/folders/1mNHEmcKJnO6hr7Wjcd7xcQ3Zmte8UlnF"],
    "p13": ["13. বাংলাদেশ ভাটিয়া রেলস্টেশন ম্যাপ+ ট্রেন মোড", "https://drive.google.com/drive/folders/13J85P8ZRDPuS-KyJrnszQfUnr-IVQVE1"],
    "p14": ["14. মধুমতি সেতু ম্যাপ", "https://drive.google.com/drive/folders/1edUHkKWxifFQsG_oluGXTjJGw2hNj1TN"],
    "p15": ["15. কুয়াকাটা টু কলাপাড়া", "https://drive.google.com/drive/folders/1ae5Qu3i2WXjMEzt9_DSK-p4eB7a3i8un"],
    "p16": ["16. গড়াই সেতু ম্যাপ মোড", "https://drive.google.com/drive/folders/1P77jKBlxGlAoPxKD2-VVnJNwpV1vfc7o"],
    "p17": ["17. বরিশাল টু খুলনা ম্যাপ", "https://drive.google.com/drive/folders/12-IlJJzulZF-B-JAnjK9ZEvLgcrxUxxL"], # পেইড
    "p18": ["18. বান্দরবান টু খাগড়াছড়ি", "https://drive.google.com/drive/folders/1uEkN7wwXE5C_NPfYTD73xYRGJ_aiBfMb"],
    "p19": ["19. ঢাকা টু সিলেট ম্যাপ", "https://drive.google.com/drive/folders/1GUeCsyvH16JW5UcZ164KU0G_exjb4RiE"],
    "p20": ["20. বাংলাদেশী গ্ৰাম ম্যাপ", "https://drive.google.com/drive/folders/1aXHSa9p-EIfseY1UOeNRCL5riKx3KkhP"],
    "p21": ["21. ঢাকা মাওয়া হাইওয়ে", "https://drive.google.com/drive/folders/1mnRyQCrAFL2pHQI6dShc1lALkta5bOi5"],
    "p22": ["22. যমুনা রেলওয়ের সেতু ম্যাপ ও ট্রেন", "https://drive.google.com/drive/folders/1yaJZx6jZTFXReuAQHVcTObkQaL6UDVRz"],
}

user_data = {}
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

def get_callback_data(base_key):
    return f"{base_key}_{uuid.uuid4().hex[:8]}"

def get_base_key(callback_data):
    return callback_data.rsplit('_', 1)[0]

def get_social_buttons():
    return [
        [InlineKeyboardButton("📺 YouTube Subscribe", url=YOUTUBE_URL)],
        [InlineKeyboardButton("📘 Facebook Page Follow", url=FB_URL)]
    ]

async def check_both_channels(user_id, context):
    try:
        member1 = await context.bot.get_chat_member(chat_id=FREE_CHANNEL_ID, user_id=user_id)
        member2 = await context.bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        status1 = member1.status in ['member', 'administrator', 'creator']
        status2 = member2.status in ['member', 'administrator', 'creator']
        return status1 and status2
    except Exception as e:
        logging.error(f"Channel check error: {e}")
        return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id in user_data:
        del user_data[user_id]
    await send_main_menu(update.message)

async def send_main_menu(target):
    keyboard = [
        [InlineKeyboardButton("🆓 ফ্রি ম্যাপ 4টি", callback_data=get_callback_data('free'))],
        [InlineKeyboardButton("💎 পেইড ম্যাপ 18টি - 40 টাকা", callback_data=get_callback_data('paid'))],
        [InlineKeyboardButton("📺 YouTube", url=YOUTUBE_URL)],
        [InlineKeyboardButton("📘 Facebook Page", url=FB_URL)],
        [InlineKeyboardButton("📢 ETS2 Channel", url=FREE_CHANNEL_URL)],
        [InlineKeyboardButton("📢 BUSSID Channel", url=CHANNEL_URL)]
    ]
    footer = f"\n\n💳 পেমেন্ট: `{BKASH}`\n📢 চ্যানেল: {CHANNEL_USERNAME}"
    text = "🚌 **BD Bussid Map Bot**\n\nনিচ থেকে ম্যাপ সিলেক্ট করো:" + footer
    await target.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown', disable_web_page_preview=True)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    base_key = get_base_key(query.data)
    footer = f"\n\n💳 পেমেন্ট: `{BKASH}`\n📢 চ্যানেল: {CHANNEL_USERNAME}"
    back_btn = [[InlineKeyboardButton("⬅️ Back to Menu", callback_data=get_callback_data('back'))]]

    if base_key == 'free':
        keyboard = [[InlineKeyboardButton(name[0], callback_data=get_callback_data(key))] for key, name in FREE_MAPS.items()]
        keyboard.append([InlineKeyboardButton("📢 খুব শীঘ্রই ফ্রি নতুন ম্যাপ এড করা হবে", url=FREE_CHANNEL_URL)])
        keyboard += back_btn
        text = "🆓 নিচ থেকে ১টি ফ্রি ম্যাপ নাও:\n\n📢 *খুব শীঘ্রই ফ্রি নতুন ম্যাপ এড করা হবে*" + footer
        await query.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown', disable_web_page_preview=True)

    elif base_key == 'paid':
        keyboard = [[InlineKeyboardButton(f"{name[0]} - 40৳", callback_data=get_callback_data(key))] for key, name in PAID_MAPS.items()] + back_btn
        text = "💎 নিচ থেকে ১টি পেইড ম্যাপ সিলেক্ট করো:" + footer
        await query.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown', disable_web_page_preview=True)

    elif base_key == 'back':
        await send_main_menu(query.message)

    elif base_key in FREE_MAPS:
        if await check_both_channels(user_id, context):
            name, link = FREE_MAPS[base_key]
            download_btn = [[InlineKeyboardButton(f"📥 {name} ডাউনলোড করুন", url=link)]] + get_social_buttons() + back_btn
            text = f"✅ **{name}**\n\nনিচের বাটনে ক্লিক করে ম্যাপ ডাউনলোড করো" + footer
            await query.message.reply_text(text, reply_markup=InlineKeyboardMarkup(download_btn), parse_mode='Markdown', disable_web_page_preview=True)
        else:
            keyboard = [
                [InlineKeyboardButton("1. ETS2 Channel", url=FREE_CHANNEL_URL)],
                [InlineKeyboardButton("2. BUSSID Channel", url=CHANNEL_URL)],
                [InlineKeyboardButton("🔄 জয়েন করে চেক করুন", callback_data=get_callback_data(base_key))]
            ] + back_btn
            text = f"⚠️ ফ্রি ম্যাপ নিতে এই 2টি চ্যানেলেই জয়েন করতে হবে।\n\n1. 👉 {FREE_CHANNEL_URL}\n2. 👉 {CHANNEL_URL}\n\nদুটোতেই জয়েন করে নিচের বাটনে চাপো।"
            await query.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), disable_web_page_preview=True)

    elif base_key in PAID_MAPS:
        user_data[user_id] = base_key
        name, link = PAID_MAPS[base_key]
        text = f"💰 **{name}**\n\nপেমেন্ট: **40 টাকা**\nবিকাশ/রকেট: `{BKASH}`\n\nটাকা পাঠিয়ে স্কিনশট এই চ্যাটে পাঠাও।" + footer
        await query.message.reply_text(text, reply_markup=InlineKeyboardMarkup(back_btn), parse_mode='Markdown', disable_web_page_preview=True)

async def screenshot_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id in user_data:
        map_key = user_data[user_id]
        map_name = PAID_MAPS[map_key][0]
        try:
            await context.bot.forward_message(chat_id=MY_ID, from_chat_id=update.message.chat_id, message_id=update.message_id)
            keyboard = [[InlineKeyboardButton("✅ Approve & Send", callback_data=f"approve_{user_id}_{map_key}")]]
            username = update.message.from_user.username or "NoUsername"
            await context.bot.send_message(
                chat_id=MY_ID,
                text=f"🔔 নতুন অর্ডার!\nUser: @{username}\nUser ID: `{user_id}`\nMap: {map_name}",
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode='Markdown'
            )
            await update.message.reply_text(f"✅ স্কিনশট পেয়েছি। `{map_name}` চেক করে ৫ মিনিটের মধ্যে লিংক দিয়ে দিবো।", parse_mode='Markdown')
            del user_data[user_id]
        except Exception as e:
            logging.error(f"Forward Error: {e}")
            await update.message.reply_text("⚠️ স্ক্রিনশট পাঠাতে সমস্যা হয়েছে। আবার পাঠাও।")
    else:
        await update.message.reply_text("⚠️ আগে উপরে ম্যাপ সিলেক্ট করুন, তারপর স্ক্রিনশট পাঠান।")

async def approve_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    _, user_id, map_key = query.data.split('_')
    user_id = int(user_id)
    name, link = PAID_MAPS[map_key]
    footer = f"\n\n💳 পেমেন্ট: `{BKASH}`\n📢 চ্যানেল: {CHANNEL_USERNAME}"
    download_btn = [[InlineKeyboardButton(f"📥 {name} ডাউনলোড করুন", url=link)]] + get_social_buttons()
    text = f"✅ পেমেন্ট Approved!\n\n**{name}**\nনিচের বাটন থেকে ডাউনলোড করো" + footer
    await context.bot.send_message(chat_id=user_id, text=text, reply_markup=InlineKeyboardMarkup(download_btn), parse_mode='Markdown', disable_web_page_preview=True)
    await query.edit_message_text("✅ লিংক পাঠানো হয়েছে।")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(CallbackQueryHandler(approve_handler, pattern='^approve_'))
    app.add_handler(MessageHandler(filters.PHOTO | filters.Document.IMAGE, screenshot_handler))
    print("BD Bussid Map Bot Running v6.0...")
    app.run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True)

if __name__ == '__main__':
    main()
