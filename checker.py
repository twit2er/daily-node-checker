import requests
import re
import random
import json
import subprocess
import time
import os
import base64
import uuid


SOURCES = [
    "https://raw.githubusercontent.com/zhuhaiuk/free-nodes/main/nodes.txt",
    "https://raw.githubusercontent.com/mahdibland/V2RayAggregator/master/sub/sub_merge.txt",
    "https://raw.githubusercontent.com/chengaopan/AutoMergePublicNodes/master/list.txt",
    "https://raw.githubusercontent.com/free-nodes/v2rayfree/main/sub"
]


def download():

    data = ""

    for url in SOURCES:

        try:
            r = requests.get(
                url,
                timeout=20
            )

            if r.status_code == 200:
                data += "\n" + r.text

        except:
            pass

    return data



def decode_base64(text):

    try:

        pad = len(text) % 4

        if pad:
            text += "=" * (4-pad)

        return base64.b64decode(
            text
        ).decode(
            errors="ignore"
        )

    except:

        return ""



def extract(text):

    result=[]


    # 原始

    result += re.findall(
        r"(?:ss|ssr|trojan|vmess|vless)://[^\s\"<>]+",
        text
    )


    # base64

    decoded = decode_base64(text)

    result += re.findall(
        r"(?:ss|ssr|trojan|vmess|vless)://[^\s\"<>]+",
        decoded
    )


    return list(set(result))



def make_config(node):


    outbound=None


    # 先處理 trojan

    if node.startswith("trojan://"):

        outbound={
            "type":"trojan",
            "tag":"proxy",
            "server":node.split("@")[-1].split(":")[0],
            "server_port":443,
            "password":node.split("://")[1].split("@")[0],
            "tls":{
                "enabled":True
            }
        }



    # ss

    elif node.startswith("ss://"):

        try:

            body=node.replace(
                "ss://",
                ""
            ).split("#")[0]


            hostpart=body.split("@")

            if len(hostpart)==2:

                user=hostpart[0]
                server=hostpart[1]

                method_password=base64.b64decode(
                    user+"=="
                ).decode()


                method,password=method_password.split(":")


                host,port=server.split(":")


                outbound={
                    "type":"shadowsocks",
                    "tag":"proxy",
                    "server":host,
                    "server_port":int(port),
                    "method":method,
                    "password":password
                }


        except:

            return None



    else:

        return None



    if not outbound:

        return None



    return {

        "log":{
            "level":"error"
        },


        "inbounds":[

            {
                "type":"mixed",
                "tag":"local",
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



def test_node(node):


    config=make_config(node)


    if not config:

        return False



    filename="test.json"


    with open(
        filename,
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
                filename
            ],

            stdout=subprocess.DEVNULL,

            stderr=subprocess.DEVNULL

        )


        time.sleep(4)



        r=requests.get(

            "https://www.gstatic.com/generate_204",

            proxies={

                "http":"http://127.0.0.1:1080",

                "https":"http://127.0.0.1:1080"

            },

            timeout=10

        )



        p.kill()



        if r.status_code==204:

            return True



    except:

        try:
            p.kill()
        except:
            pass



    return False




def main():


    print("開始下載")


    data=download()


    nodes=extract(data)


    random.shuffle(nodes)


    print(
        "候選:",
        len(nodes)
    )


    alive=[]



    for node in nodes[:300]:


        print(
            "測試:",
            node[:50]
        )



        if test_node(node):


            print(
                "成功"
            )


            alive.append(node)



        if len(alive)>=50:

            break



    print(
        "有效:",
        len(alive)
    )



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



if __name__=="__main__":

    main()
