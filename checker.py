import requests
import re
import random
import json
import subprocess
import time
import base64
import os


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

        except Exception:
            pass

    return text



def extract(text):

    nodes = re.findall(
        r"(?:ss|trojan)://[^\s\"<>]+",
        text
    )

    return list(set(nodes))



def make_config(node):

    if node.startswith("trojan://"):

        try:

            info=node.replace(
                "trojan://",
                ""
            )

            password,server=info.split("@")

            host=server.split(":")[0]


            return {

                "log":{
                    "level":"error"
                },

                "inbounds":[
                    {
                        "type":"mixed",
                        "listen":"127.0.0.1",
                        "listen_port":1080
                    }
                ],

                "outbounds":[

                    {
                        "type":"trojan",
                        "server":host,
                        "server_port":443,
                        "password":password,
                        "tls":{
                            "enabled":True
                        }
                    }

                ]

            }


        except:

            return None


    return None



def test(node):

    config=make_config(node)


    if not config:
        return False


    with open(
        "test.json",
        "w",
        encoding="utf8"
    ) as f:

        json.dump(
            config,
            f
        )


    p=None

    try:

        p=subprocess.Popen(

            [
                "sing-box",
                "run",
                "-c",
                "test.json"
            ],

            stdout=subprocess.DEVNULL,

            stderr=subprocess.DEVNULL

        )


        time.sleep(2)


        r=requests.get(

            "https://www.gstatic.com/generate_204",

            proxies={

                "http":"http://127.0.0.1:1080",

                "https":"http://127.0.0.1:1080"

            },

            timeout=5

        )


        return r.status_code==204


    except:

        return False


    finally:

        if p:

            p.kill()



def main():

    print("下載節點")

    data=download()


    nodes=extract(data)


    random.shuffle(nodes)


    print(
        "候選數:",
        len(nodes)
    )


    alive=[]


    # 只測20個，確認流程

    for node in nodes[:20]:

        print(
            "測試:",
            node[:50]
        )


        if test(node):

            print("OK")

            alive.append(node)


        else:

            print("FAIL")



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
            f.write(n+"\n")



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
