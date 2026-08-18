import os
import telebot

TOKEN = os.environ["BOT_TOKEN"]
ADMIN_ID = int(os.environ["ADMIN_ID"])

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start"])
def start(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(
            message,
            "❌ 無權限使用"
        )
        return

    bot.reply_to(
        message,
        """
✅ Daily Node Checker

功能：

/start
重新獲取節點

目前：
每天自動抓取節點
自動篩選
發送優選節點

管理員模式已開啟
        """
    )


bot.infinity_polling()
