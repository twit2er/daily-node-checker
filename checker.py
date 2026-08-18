import requests
import re
import random
import base64
import subprocess
import json
import os
import time


SOURCES = [
    "https://raw.githubusercontent.com/zhuhaiuk/free-nodes/main/nodes.txt",
    "https://raw.githubusercontent.com/mahdibland/V2RayAggregator/master/sub/sub_merge.txt",
    "https://raw.githubusercontent.com/chengaopan/AutoMergePublicNodes/master/list.txt",
    "https://raw.githubusercontent.com/free-nodes/v2rayfree/main/sub"
]


def download():

    text = ""

    for url in SOURCES:
        try:
            r = requests.get(url, timeout=15)

            if r.status_code == 200:
                text += "\n" + r.text

        except:
            pass

    return text



def extract(text):

    return list(set(
        re.findall(
            r"(?:vmess|vless|trojan|ss|ssr)://[^\s\"<>]+",
            text
        )
    ))



def test_node(node):

    # 目前先保留格式
    # 真正測試需要xray/sing-box解析

    if len(node) < 20:
        return False

    return True



def main():

    print("抓取節點")

    data = download()

    nodes = extract(data)

    random.shuffle(nodes)


    alive=[]


    for n in nodes:

        if test_node(n):

            alive.append(n)

            print(
                "保留:",
                len(alive)
            )


        if len(alive)>=50:
            break



    print(
        "生成:",
        len(alive)
    )


    with open(
        "nodes.txt",
        "w",
        encoding="utf-8"
    ) as f:

        for n in alive:
            f.write(n+"\n")



    sub64 = base64.b64encode(
        "\n".join(alive).encode()
    ).decode()



    with open(
        "sub.txt",
        "w",
        encoding="utf-8"
    ) as f:

        f.write(sub64)



if __name__=="__main__":
    main()
