import requests
import re
import random
import json
import subprocess
import time
import os
import base64


SOURCES = [
    "https://raw.githubusercontent.com/zhuhaiuk/free-nodes/main/nodes.txt",
    "https://raw.githubusercontent.com/mahdibland/V2RayAggregator/master/sub/sub_merge.txt",
    "https://raw.githubusercontent.com/chengaopan/AutoMergePublicNodes/master/list.txt",
]


def download():

    text = ""

    for url in SOURCES:
        try:
            r = requests.get(
                url,
                timeout=15
            )

            if r.status_code == 200:
                text += "\n" + r.text

        except:
            pass

    return text



def extract(text):

    nodes = re.findall(
        r"(?:ss|trojan)://[^\s\"<>]+",
        text
    )

    return list(set(nodes))



def build_config(node):

    outbound = None


    if node.startswith("ss://"):

        # sing-box 支持直接 URL

        outbound = {
            "type": "shadowsocks",
            "tag": "proxy",
            "server": node
        }


    elif node.startswith("trojan://"):

        outbound = {
            "type": "trojan",
            "tag": "proxy",
            "server": node
        }


    if not outbound:
        return None


    config = {

        "log": {
            "level":"error"
        },

        "inbounds":[
            {
                "type":"mixed",
                "tag":"mixed-in",
                "listen":"127.0.0.1",
                "listen_port":1080
            }
        ],

        "outbounds":[
            outbound,
            {
                "type":"direct",
                "tag":"direct"
            }
        ]
    }


    return config



def test_node(node):

    config = build_config(node)

    if not config:
        return False


    with open(
        "temp.json",
        "w",
        encoding="utf8"
    ) as f:

        json.dump(
            config,
            f
        )


    try:

        p=subprocess.Popen(
            [
                "sing-box",
                "run",
                "-c",
                "temp.json"
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )


        time.sleep(3)


        r=requests.get(
            "https://www.gstatic.com/generate_204",
            proxies={
                "http":"http://127.0.0.1:1080",
                "https":"http://127.0.0.1:1080"
            },
            timeout=8
        )


        p.kill()


        return r.status_code==204


    except Exception:

        try:
            p.kill()
        except:
            pass

        return False



def main():

    print("抓取")


    data=download()


    nodes=extract(data)


    random.shuffle(nodes)


    print(
        "候選:",
        len(nodes)
    )


    alive=[]


    for node in nodes[:200]:

        print(
            "測試",
            node[:40]
        )


        if test_node(node):

            alive.append(node)

            print(
                "成功:",
                len(alive)
            )


        if len(alive)>=50:
            break



    with open(
        "nodes.txt",
        "w",
        encoding="utf8"
    ) as f:

        for n in alive:
            f.write(
                n+"\n"
            )


    sub=base64.b64encode(
        "\n".join(alive).encode()
    ).decode()


    with open(
        "sub.txt",
        "w",
        encoding="utf8"
    ) as f:

        f.write(sub)



    print(
        "完成:",
        len(alive)
    )



if __name__=="__main__":

    main()
