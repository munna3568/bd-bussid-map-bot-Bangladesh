import os
import logging
import uuid
import base64
import sqlite3
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from telegram.error import Forbidden, BadRequest

TOKEN = os.getenv("TOKEN")
CHANNEL_ID = -1003741615712
FREE_CHANNEL_ID = -1004392467475
CHANNEL_USERNAME = "@bdbussidlover"
FREE_CHANNEL_URL = "https://t.me/bdets2loverandroid"
CHANNEL_URL = "https://t.me/bdbussidlover"
YOUTUBE_URL = "https://www.youtube.com/@NHMMunna"
FB_URL = "https://www.facebook.com/profile.php?id=61587406053752"
BKASH = "01832533534"
MY_ID = 7304092520
DB_FILE = "bot_data.db"

# ==================== DATA ====================
FREE_MAPS = {
    "map1": ["1. ঢাকা টু রংপুর", "https://drive.google.com/drive/folders/1MqUuSO5n_o5_0WzUeyE3RQen6FXutiRW"],
    "map2": ["2. Bangladesh 300 Fit", "https://drive.google.com/drive/folders/1-jNRfPjI4OlGfDQEglfMuCk2mtj7hedV"],
    "map3": ["3. যমুনা সেতু ম্যাপ", "https://drive.google.com/file/d/123BVMajNDXwXaz7x3Y5woUKY1y4d6GAj/view?usp=drivesdk"],
    "map4": ["4. রাজশাহী টু বরিশাল", "https://drive.google.com/drive/folders/1FheeZ49p62z4YWxWKSU22R_2RjC4iALg"],
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
    "p17": ["17. বরিশাল টু খুলনা ম্যাপ", "https://drive.google.com/drive/folders/12-IlJJzulZF-B-JAnjK9ZEvLgcrxUxxL"],
    "p18": ["18. বান্দরবান টু খাগড়াছড়ি", "https://drive.google.com/drive/folders/1uEkN7wwXE5C_NPfYTD73xYRGJ_aiBfMb"],
    "p19": ["19. ঢাকা টু সিলেট ম্যাপ", "https://drive.google.com/drive/folders/1GUeCsyvH16JW5UcZ164KU0G_exjb4RiE"],
    "p20": ["20. বাংলাদেশী গ্ৰাম ম্যাপ", "https://drive.google.com/drive/folders/1aXHSa9p-EIfseY1UOeNRCL5riKx3KkhP"],
    "p21": ["21. ঢাকা মাওয়া হাইওয়ে", "https://drive.google.com/drive/folders/1mnRyQCrAFL2pHQI6dShc1lALkta5bOi5"],
    "p22": ["22. যমুনা রেলওয়ের সেতু ম্যাপ ও ট্রেন", "https://drive.google.com/drive/folders/1yaJZx6jZTFXReuAQHVcTObkQaL6UDVRz"],
}
BUS_MODS = {
    "bm1": ["1. হানিফ", "coming_soon"], "bm2": ["2. শ্যামলী", "coming_soon"], "bm3": ["3. নাবিল", "coming_soon"],
    "bm4": ["4. এস আর লাইন", "coming_soon"], "bm5": ["5. এনা", "coming_soon"], "bm6": ["6. সি লাইন", "coming_soon"],
    "bm7": ["7. বিআরটিসি", "coming_soon"], "bm8": ["8. ন্যাশনাল ট্রেভেল", "coming_soon"], "bm9": ["9. সকাল সন্ধ্যা", "coming_soon"],
    "bm10": ["10. এনা ২.০", "coming_soon"], "bm11": ["11. সৌদিয়া মার্সিডিজ এসি", "coming_soon"], "bm12": ["12. গ্ৰামীন ট্রেভেলস", "coming_soon"],
    "bm13": ["13. হানিফ মার্সিডিজ বেঞ্জ", "coming_soon"],
}
BUS_SKINS = {
    "bs1": ["1. গেমের প্রথম বাস স্কিন", "coming_soon"],
    "bs2": ["2. গেমের দ্বিতীয় বাস স্কিন", "coming_soon"],
}
OBBS = {
    "obb1": ["1. স্পিড ট্রাফিক", "https://tsegaming.com/bd-map-v4-4-1-speed-traffic-obb-setup"],
    "obb2": ["2. মিডিয়াম স্পিড ট্রাফিক", "https://tsegaming.com/bd-ets2-v2-traffic-obb-v4-2"],
    "obb3": ["3. হাই ট্রাফিক স্পিড", "https://youtu.be/FKfpC8hXA9k"],
    "obb4": ["4. ৩.৭.১ বাংলাদেশের ওবিবি", "https://youtu.be/t_tawZcSE98?si=EDQ6xBePvUF3tkds"],
    "obb5": ["5. 4K Graphics OBB", "https://tsebussid.blogspot.com/2026/07/4k-graphics-obb-2026.html"],
    "obb6": ["6. মাল্টিপ্লয়ার OBB", "https://argamezoneofficial.blogspot.com/2026/07/download-high-speed-traffic-obb-v2-for.html"],
    "obb7": ["7. ৬ জিবি রেম OBB", "https://www.gamingwithsajedul.website/2026/07/apk-obb-bd-map-guide.html"],
}
# ==================== END DATA ====================

user_data = {}
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, first_join TEXT)''')
    conn.commit()
    conn.close()

def save_user(user_id):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try: c.execute("INSERT INTO users (user_id, first_join) VALUES (?,?)", (user_id, today)); conn.commit()
    except sqlite3.IntegrityError: pass
    conn.close()

def get_stats():
    conn = sqlite3.connect(DB_FILE); c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM users"); total = c.fetchone()[0]
    today = datetime.now().strftime("%Y-%m-%d")
    c.execute("SELECT COUNT(*) FROM users WHERE first_join LIKE?", (f"{today}%",)); today_new = c.fetchone()[0]
    conn.close(); return total, today_new

def encode_data(user_id, map_key):
    data = f"{user_id}:{map_key}"
    encoded = base64.urlsafe_b64encode(data.encode()).decode()
    return encoded.rstrip("=")

def decode_data(encoded):
    padding = '=' * (-len(encoded) % 4)
    data = base64.urlsafe_b64decode(encoded + padding).decode()
    user_id, map_key = data.split(':')
    return int(user_id), map_key

def get_callback_data(base_key): return f"{base_key}_{uuid.uuid4().hex[:8]}"
def get_base_key(callback_data): return callback_data.rsplit('_', 1)[0]
def get_social_buttons(): return [[InlineKeyboardButton("📺 YouTube Subscribe", url=YOUTUBE_URL)], [InlineKeyboardButton("📘 Facebook Page Follow", url=FB_URL)]]

async def check_both_channels(user_id, context):
    try:
        member1 = await context.bot.get_chat_member(chat_id=FREE_CHANNEL_ID, user_id=user_id)
        member2 = await context.bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        return member1.status in ['member', 'administrator', 'creator'] and member2.status in ['member', 'administrator', 'creator']
    except Exception as e: logging.error(f"Channel check error: {e}"); return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    save_user(user_id)
    if user_id in user_data: del user_data[user_id]
    await send_main_menu(update.message)

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id!= MY_ID: await update.message.reply_text("⚠️ এই কমান্ড শুধু এডমিনের জন্য"); return
    total, today_new = get_stats()
    await update.message.reply_text(f"📊 **বট স্ট্যাটস**\n\n👥 মোট ইউজার: `{total}` জন\n🆕 আজকের নতুন: `{today_new}` জন", parse_mode='Markdown')

async def users_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id!= MY_ID: await update.message.reply_text("⚠️ এই কমান্ড শুধু এডমিনের জন্য"); return
    conn = sqlite3.connect(DB_FILE); c = conn.cursor()
    c.execute("SELECT user_id, first_join FROM users ORDER BY first_join DESC LIMIT 100"); users = c.fetchall(); conn.close()
    if not users: await update.message.reply_text("এখনো কোনো ইউজার নাই"); return
    text = f"👥 **সর্বশেষ {len(users)} জন ইউজার**\n\n"
    for i, (uid, date) in enumerate(users, 1): text += f"{i}. `ID: {uid}`\n 📅 {date}\n\n"
    await update.message.reply_text(text, parse_mode='Markdown')

async def send_main_menu(target):
    keyboard = [
        [InlineKeyboardButton("🚌 বাস মোড 13টি - 200-240 KM/H", callback_data=get_callback_data('busmod'))],
        [InlineKeyboardButton("🎨 বাস স্কিন 2টি", callback_data=get_callback_data('busskin'))],
        [InlineKeyboardButton("📦 OBB 7টি", callback_data=get_callback_data('obb'))],
        [InlineKeyboardButton("🆓 ম্যাপ 4টি", callback_data=get_callback_data('free'))],
        [InlineKeyboardButton("💎 পেইড ম্যাপ 18টি - 40 টাকা", callback_data=get_callback_data('paid'))],
        [InlineKeyboardButton("📺 YouTube", url=YOUTUBE_URL)],
        [InlineKeyboardButton("📘 Facebook Page", url=FB_URL)],
        [InlineKeyboardButton("📢 ETS2 Channel", url=FREE_CHANNEL_URL)],
        [InlineKeyboardButton("📢 BUSSID Channel", url=CHANNEL_URL)]
    ]
    footer = f"\n\n💳 সেন্ড মানি: `{BKASH}`\n📢 চ্যানেল: {CHANNEL_USERNAME}"
    text = "🚌 **BD Bussid Map Bot v7.8**\n\nনিচ থেকে সিলেক্ট করো:" + footer
    await target.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown', disable_web_page_preview=True)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query; await query.answer(); user_id = query.from_user.id; base_key = get_base_key(query.data)
    if query.data.startswith('a_'): await approve_handler(update, context); return
    if query.data.startswith('r_'): await reject_handler(update, context); return
    footer = f"\n\n💳 সেন্ড মানি: `{BKASH}`\n📢 চ্যানেল: {CHANNEL_USERNAME}"
    back_btn = [[InlineKeyboardButton("⬅️ Back to Menu", callback_data=get_callback_data('back'))]]
    if base_key == 'busmod':
        keyboard = [[InlineKeyboardButton(name[0] + " - 200-240 KM/H", callback_data=get_callback_data(key))] for key, name in BUS_MODS.items()] + back_btn
        text = "🚌 **বাস মোড 13টি**\nSpeed: 200-240 KM/H" + footer
        await query.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')
    elif base_key == 'busskin':
        keyboard = [[InlineKeyboardButton(name[0], callback_data=get_callback_data(key))] for key, name in BUS_SKINS.items()] + back_btn
        text = "🎨 **বাস স্কিন 2টি**\nপ্রতিটার ভিতরে 13টা বাসের স্কিন আছে" + footer
        await query.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')
    elif base_key == 'obb':
        keyboard = [[InlineKeyboardButton(name[0], callback_data=get_callback_data(key))] for key, name in OBBS.items()] + back_btn
        text = "📦 **OBB 7টি**\nনিচ থেকে সিলেক্ট করো:" + footer
        await query.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')
    elif base_key in BUS_MODS or base_key in BUS_SKINS or base_key in OBBS:
        if await check_both_channels(user_id, context):
            data_dict = BUS_MODS if base_key in BUS_MODS else BUS_SKINS if base_key in BUS_SKINS else OBBS
            name, link = data_dict[base_key]
            if link == "coming_soon":
                text = f"🚧 **{name}**\n\nখুব শীঘ্রই লিংক এড করা হবে।\nআপডেট পেতে চ্যানেল ফলো করো।" + footer
                download_btn = get_social_buttons() + back_btn
            else:
                download_btn = [[InlineKeyboardButton(f"📥 {name} ডাউনলোড", url=link)]] + get_social_buttons() + back_btn
                text = f"✅ **{name}**\n\nনিচের বাটনে ক্লিক করে ডাউনলোড করো" + footer
            await query.message.reply_text(text, reply_markup=InlineKeyboardMarkup(download_btn), parse_mode='Markdown', disable_web_page_preview=True)
        else:
            keyboard = [[InlineKeyboardButton("1. ETS2 Channel", url=FREE_CHANNEL_URL)], [InlineKeyboardButton("2. BUSSID Channel", url=CHANNEL_URL)], [InlineKeyboardButton("🔄 জয়েন করে চেক করুন", callback_data=get_callback_data(base_key))]] + back_btn
            text = f"⚠️ ডাউনলোড করতে এই 2টি চ্যানেলেই জয়েন করতে হবে।\n\n1. 👉 {FREE_CHANNEL_URL}\n2. 👉 {CHANNEL_URL}\n\nদুটোতেই জয়েন করে নিচের বাটনে চাপো।"
            await query.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), disable_web_page_preview=True)
    elif base_key == 'free':
        keyboard = [[InlineKeyboardButton(name[0], callback_data=get_callback_data(key))] for key, name in FREE_MAPS.items()]
        keyboard.append([InlineKeyboardButton("📢 খুব শীঘ্রই নতুন ম্যাপ এড করা হবে", url=FREE_CHANNEL_URL)])
        keyboard += back_btn
        text = "🆓 নিচ থেকে ১টি ম্যাপ নাও:\n\n📢 *খুব শীঘ্রই নতুন ম্যাপ এড করা হবে*" + footer
        await query.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown', disable_web_page_preview=True)
    elif base_key == 'paid':
        keyboard = [[InlineKeyboardButton(f"{name[0]} - 40৳", callback_data=get_callback_data(key))] for key, name in PAID_MAPS.items()] + back_btn
        text = "💎 নিচ থেকে ১টি পেইড ম্যাপ সিলেক্ট করো:" + footer
        await query.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')
    elif base_key == 'back': await send_main_menu(query.message)
    elif base_key in FREE_MAPS:
        if await check_both_channels(user_id, context):
            name, link = FREE_MAPS[base_key]
            download_btn = [[InlineKeyboardButton(f"📥 {name} ডাউনলোড করুন", url=link)]] + get_social_buttons() + back_btn
            text = f"✅ **{name}**\n\nনিচের বাটনে ক্লিক করে ম্যাপ ডাউনলোড করো" + footer
            await query.message.reply_text(text, reply_markup=InlineKeyboardMarkup(download_btn), parse_mode='Markdown', disable_web_page_preview=True)
        else:
            keyboard = [[InlineKeyboardButton("1. ETS2 Channel", url=FREE_CHANNEL_URL)], [InlineKeyboardButton("2. BUSSID Channel", url=CHANNEL_URL)], [InlineKeyboardButton("🔄 জয়েন করে চেক করুন", callback_data=get_callback_data(base_key))]] + back_btn
            text = f"⚠️ ডাউনলোড করতে এই 2টি চ্যানেলেই জয়েন করতে হবে।\n\n1. 👉 {FREE_CHANNEL_URL}\n2. 👉 {CHANNEL_URL}\n\nদুটোতেই জয়েন করে নিচের বাটনে চাপো।"
            await query.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), disable_web_page_preview=True)
    elif base_key in PAID_MAPS:
        user_data[user_id] = base_key; name, link = PAID_MAPS[base_key]
        text = f"💰 **{name}**\n\nসেন্ড মানি: **40 টাকা**\nবিকাশ/রকেট: `{BKASH}`\n\nটাকা পাঠিয়ে স্কিনশট এই চ্যাটে পাঠাও।" + footer
        await query.message.reply_text(text, reply_markup=InlineKeyboardMarkup(back_btn), parse_mode='Markdown')

async def screenshot_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id in user_data:
        map_key = user_data[user_id]; map_name = PAID_MAPS[map_key][0]
        try:
            photo = update.message.photo[-1].file_id
            username = update.message.from_user.username or update.message.from_user.first_name
            encoded = encode_data(user_id, map_key)
            caption = f"🔔 নতুন অর্ডার!\nUser: @{username}\nUser ID: `{user_id}`\nMap: {map_name}"
            keyboard = [[InlineKeyboardButton("✅ Approve & Send", callback_data=f"a_{encoded}")], [InlineKeyboardButton("❌ Reject - ভুল স্ক্রিনশট", callback_data=f"r_{encoded}")]]
            await context.bot.send_photo(chat_id=MY_ID, photo=photo, caption=caption, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')
            await update.message.reply_text(f"✅ স্কিনশট পেয়েছি। `{map_name}` চেক করে ৫ মিনিটের মধ্যে লিংক দিয়ে দিবো।", parse_mode='Markdown')
            del user_data[user_id]
        except Exception as e: logging.error(f"Send Photo Error: {e}"); await update.message.reply_text("⚠️ স্ক্রিনশট পাঠাতে সমস্যা হয়েছে। আবার পাঠাও।")
    else: await update.message.reply_text("⚠️ আগে উপরে ম্যাপ সিলেক্ট করুন, তারপর স্ক্রিনশট পাঠান।")

# ===== NEW: UNKNOWN TEXT HANDLER =====
async def unknown_text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id in user_data:
        await update.message.reply_text("⚠️ আগে স্ক্রিনশট পাঠান। অথবা `Back to Menu` চেপে বের হয়ে আসুন।", parse_mode='Markdown')
        return

    keyboard = [[InlineKeyboardButton("🔄 /start - বট চালু করুন", callback_data=get_callback_data('back'))]]
    text = "❌ ভাই বুঝলাম না।\n\nইংরেজিতে লেখা `Menu` বাটনে চাপুন অথবা `/start` লিখে পাঠান।\nবট চালু হবে।"
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')
# ===== END NEW =====

async def approve_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query; await query.answer(); user_id = None
    try:
        _, encoded = query.data.split('_', 1); user_id, map_key = decode_data(encoded)
        name, link = PAID_MAPS[map_key]; footer = f"\n\n💳 সেন্ড মানি: `{BKASH}`\n📢 চ্যানেল: {CHANNEL_USERNAME}"
        download_btn = [[InlineKeyboardButton(f"📥 {name} ডাউনলোড করুন", url=link)]] + get_social_buttons()
        text = f"✅ পেমেন্ট Approved!\n\n**{name}**\nনিচের বাটন থেকে ডাউনলোড করো" + footer
        await context.bot.send_message(chat_id=user_id, text=text, reply_markup=InlineKeyboardMarkup(download_btn), parse_mode='Markdown', disable_web_page_preview=True)
        await context.bot.send_message(chat_id=MY_ID, text=f"✅ **Approved Done**\n\nUser ID: `{user_id}`\nMap: {name}\n\nইউজারকে লিংক পাঠানো হয়েছে।", parse_mode='Markdown')
        await query.edit_message_reply_markup(reply_markup=None)
    except Forbidden:
        await context.bot.send_message(chat_id=MY_ID, text=f"❌ **Approved Failed!**\n\nইউজার বটকে Block করেছে বা /start দেয়নি।\nUser ID: `{user_id}`", parse_mode='Markdown');
        await query.edit_message_reply_markup(reply_markup=None)
    except Exception as e: logging.error(f"Approve Error: {e}")

async def reject_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query; await query.answer(); user_id = None
    try:
        _, encoded = query.data.split('_', 1); user_id, map_key = decode_data(encoded)
        name = PAID_MAPS[map_key][0]
        text = f"⚠️ আপনার পাঠানো স্ক্রিনশটটি সঠিক নয়।\n\n**ম্যাপ:** {name}\n\nঅনুগ্রহ করে বিকাশ/রকেট `{BKASH}` নাম্বারে 40 টাকা সেন্ড মানি করে সঠিক ট্রানজেকশন স্ক্রিনশট আবার পাঠান।"
        await context.bot.send_message(chat_id=user_id, text=text, parse_mode='Markdown')
        await context.bot.send_message(chat_id=MY_ID, text=f"❌ **Rejected Done**\n\nUser ID: `{user_id}`\nMap: {name}\n\nইউজারকে ভুল স্ক্রিনশট নোটিশ পাঠানো হয়েছে।", parse_mode='Markdown')
        await query.edit_message_reply_markup(reply_markup=None)
    except Forbidden:
        await context.bot.send_message(chat_id=MY_ID, text=f"❌ **Rejected Failed!**\n\nইউজার বটকে Block করেছে বা /start দেয়নি।\nUser ID: `{user_id}`", parse_mode='Markdown');
        await query.edit_message_reply_markup(reply_markup=None)
    except Exception as e: logging.error(f"Reject Error: {e}")

def main():
    init_db()
    if not TOKEN:
        print("ERROR: TOKEN not found in Environment Variables")
        return
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(CommandHandler("users", users_list))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.PHOTO | filters.Document.ALL, screenshot_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, unknown_text_handler)) # NEW LINE
    print("BD Bussid Map Bot Running v7.8...")
    app.run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True)

if __name__ == '__main__': main()
