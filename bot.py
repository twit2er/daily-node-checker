import os
import telebot

TOKEN = os.environ["BOT_TOKEN"]
ADMIN_ID = int(os.environ["ADMIN_ID"])

bot = telebot.TeleBot(TOKEN)


def get_nodes():

    try:
        with open(
            "nodes.txt",
            "r",
            encoding="utf-8"
        ) as f:
            nodes = f.read()

        return nodes[:4000]

    except:
        return "❌ 节点文件不存在，请等待更新"


@bot.message_handler(commands=["start"])
def start(message):

    if message.from_user.id != ADMIN_ID:
        bot.reply_to(
            message,
            "❌ 无权限"
        )
        return


    bot.reply_to(
        message,
        """
✅ Twit2le Node Checker

功能：

/start
查看功能

/nodes
获取50个优选节点


自动更新：
✅ 每8小时抓取
✅ GitHub节点源
✅ 自动去重

管理员模式开启
"""
    )


@bot.message_handler(commands=["nodes"])
def nodes(message):

    if message.from_user.id != ADMIN_ID:
        return


    data = get_nodes()

    bot.reply_to(
        message,
        "✅ 最新50个节点：\n\n" + data
    )


bot.infinity_polling()
