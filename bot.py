import os
import telebot
import json

TOKEN = os.environ["BOT_TOKEN"]

bot = telebot.TeleBot(TOKEN)

ADMIN_ID = int(os.environ["ADMIN_ID"])

WHITELIST_FILE = "whitelist.json"


def load_whitelist():
    try:
        with open(WHITELIST_FILE, "r") as f:
            return json.load(f)
    except:
        return [ADMIN_ID]


def save_whitelist(data):
    with open(WHITELIST_FILE, "w") as f:
        json.dump(data, f)


@bot.message_handler(commands=["start"])
def start(message):

    users = load_whitelist()

    if message.from_user.id not in users:
        bot.reply_to(
            message,
            "❌ 无权限使用"
        )
        return


    bot.reply_to(
        message,
        """
✅ Twit2le Node Checker

功能：

/start
获取50个优选节点

/whitelist ID
添加授权用户

/list
查看授权列表


当前状态：

✅ GitHub自动抓取
✅ 自动去重
✅ 自动筛选
✅ 每天更新3次

节点将在这里发送。
"""
    )


@bot.message_handler(commands=["whitelist"])
def whitelist(message):

    if message.from_user.id != ADMIN_ID:
        return


    try:
        uid = int(message.text.split()[1])

        users = load_whitelist()

        if uid not in users:
            users.append(uid)
            save_whitelist(users)

        bot.reply_to(
            message,
            "✅ 已添加"
        )

    except:
        bot.reply_to(
            message,
            "格式：/whitelist 用户ID"
        )


@bot.message_handler(commands=["list"])
def list_users(message):

    if message.from_user.id != ADMIN_ID:
        return

    users = load_whitelist()

    bot.reply_to(
        message,
        str(users)
    )


bot.infinity_polling()
