import os
import requests
import telebot


TOKEN = os.environ["BOT_TOKEN"]
ADMIN_ID = int(os.environ["ADMIN_ID"])

bot = telebot.TeleBot(TOKEN)


NODE_URL = "https://raw.githubusercontent.com/twit2er/daily-node-checker/main/nodes.txt"


def get_nodes():

    try:
        r = requests.get(
            NODE_URL,
            timeout=20
        )

        if r.status_code == 200:
            return r.text[:4000]

        return "❌ 節點文件讀取失敗"

    except:
        return "❌ 網絡錯誤"


@bot.message_handler(commands=["start"])
def start(message):

    if message.from_user.id != ADMIN_ID:
        bot.reply_to(
            message,
            "❌ 無權限"
        )
        return


    bot.reply_to(
        message,
        "⏳ 正在獲取最新50個節點..."
    )


    nodes = get_nodes()


    bot.send_message(
        message.chat.id,
        "✅ 最新節點：\n\n" + nodes
    )


bot.infinity_polling()
