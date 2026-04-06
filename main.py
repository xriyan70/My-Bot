import telebot
import requests
import time
from telebot import types

# ১. সেটিংস
API_TOKEN = '8678067992:AAEDkPkmtuz86YnrMJcnIVcp19tL52tkyRk'
CHANNEL_USERNAME = '@developer_of_maruf' 
PHOTO_URL = "https://i.ibb.co/6R0VjY8/banner.jpg" 
WHATSAPP_LINK = "https://wa.me/8801621743805"

bot = telebot.TeleBot(API_TOKEN)

def check_join(chat_id):
    try:
        status = bot.get_chat_member(CHANNEL_USERNAME, chat_id).status
        return status in ['member', 'administrator', 'creator']
    except Exception as e:
        print(f"Error checking join: {e}")
        return False

@bot.message_handler(commands=['start'])
def welcome(message):
    chat_id = message.chat.id
    if check_join(chat_id):
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🛒 অর্ডার করুন (WhatsApp)", url=WHATSAPP_LINK))
        
        # ছবি পাঠাতে চেষ্টা করবে, না পারলে শুধু লেখা পাঠাবে
        try:
            bot.send_photo(chat_id, PHOTO_URL, caption="✨ **মৃত্তিকা অরিজিনাল হলুদ** ✨\n১০০% খাঁটি ও ভেজাল মুক্ত।", parse_mode="Markdown", reply_markup=markup)
        except:
            bot.send_message(chat_id, "✨ **মৃত্তিকা অরিজিনাল হলুদ** ✨\n\n✅ ভেরিফিকেশন সফল! SMS পাঠাতে নাম্বার দিন:", reply_markup=markup)
    else:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("📢 Join Channel", url=f"https://t.me/developer_of_maruf"))
        bot.send_message(chat_id, "❌ আগে আমাদের চ্যানেলে জয়েন করুন!", reply_markup=markup)

if __name__ == "__main__":
    bot.infinity_polling(skip_pending=True)
