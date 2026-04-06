def send_bomber(message):
    try:
        amount = int(message.text)
        num = user_data[message.chat.id]

        if amount > 100:
            amount = 100

        bot.send_message(message.chat.id, f"🚀 {num} নাম্বারে {amount}টি SMS পাঠানো শুরু হয়েছে...")

        success = 0

        for i in range(amount):
            try:
                # এখানে তোমার API call থাকবে (legal use হলে)
                res = requests.post("YOUR_API", json={"phone": num}, timeout=10)

                if res.status_code == 200:
                    success += 1

                time.sleep(2)

            except:
                continue

        # 👉 loop শেষ হওয়ার পর result দেখাবে
        if success > 0:
            bot.send_message(message.chat.id, f"✅ {success} টি SMS সফলভাবে পাঠানো হয়েছে!")
        else:
            bot.send_message(message.chat.id, "❌ কোনো SMS পাঠানো যায়নি!")

        bot.send_message(message.chat.id, "🔁 আবার করতে /start লিখুন")

    except:
        bot.send_message(message.chat.id, "❌ শুধু সংখ্যা দিন")
