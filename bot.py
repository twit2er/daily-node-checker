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
            return r.text

        return "❌ 節點文件讀取失敗"

    except Exception as e:
        return f"❌ 錯誤: {e}"



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

命令：

/nodes
獲取最新50個優選節點

/start
查看功能

目前狀態：
✅ GitHub自動更新
✅ 節點去重
✅ 定時更新

管理員模式開啟
"""
    )



@bot.message_handler(commands=["nodes"])
def nodes(message):

    if message.from_user.id != ADMIN_ID:
        bot.reply_to(
            message,
            "❌ 無權限"
        )
        return


    bot.send_message(
        message.chat.id,
        "⏳ 正在獲取節點..."
    )


    data = get_nodes()


    if len(data) > 3800:
        data = data[:3800]


    bot.send_message(
        message.chat.id,
        data
    )



bot.infinity_polling()
