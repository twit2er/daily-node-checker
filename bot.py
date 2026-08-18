import os
import requests
import telebot


TOKEN = os.environ["BOT_TOKEN"]

ADMIN_ID = int(os.environ["ADMIN_ID"])


bot = telebot.TeleBot(TOKEN)


NODE_URL = (
    "https://raw.githubusercontent.com/"
    "twit2er/daily-node-checker/"
    "main/nodes.txt"
)



def check_user(message):

    return message.from_user.id == ADMIN_ID



def get_nodes():

    try:

        r = requests.get(
            NODE_URL,
            timeout=15
        )

        if r.status_code == 200:

            return r.text[:4000]

        else:

            return "❌ 节点文件读取失败"


    except Exception as e:

        return "❌ 获取节点失败"



@bot.message_handler(commands=["start"])
def start(message):

    if not check_user(message):

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

/nodes
获取最新50个优选节点


当前状态：

✅ GitHub自动抓取
✅ 自动去重
✅ 支持：

vmess
vless
trojan
ss
ssr
hysteria2


自动更新：
每天3次


管理员模式开启
"""
    )



@bot.message_handler(commands=["nodes"])
def nodes(message):

    if not check_user(message):

        return


    data = get_nodes()


    bot.reply_to(
        message,
        "✅ 最新节点：\n\n" + data
    )



bot.infinity_polling()
