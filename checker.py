import requests
import re
import random
import subprocess
import json
import time
import base64
import os


SOURCES=[
"https://raw.githubusercontent.com/zhuhaiuk/free-nodes/main/nodes.txt",
"https://raw.githubusercontent.com/mahdibland/V2RayAggregator/master/sub/sub_merge.txt",
"https://raw.githubusercontent.com/chengaopan/AutoMergePublicNodes/master/list.txt",
]


def download():

    data=""

    for u in SOURCES:

        try:

            r=requests.get(
                u,
                timeout=15
            )

            if r.status_code==200:
                data+=r.text

        except:
            pass

    return data



def extract(text):

    return list(set(
        re.findall(
            r"(?:ss|trojan)://[^\s]+",
            text
        )
    ))



def test(node):

    # 臨時跳過複雜節點
    # 只保留格式測試

    if len(node)<30:
        return False

    return True



def main():

    print("download")

    data=download()

    nodes=extract(data)

    random.shuffle(nodes)


    alive=[]


    for n in nodes:

        if test(n):

            alive.append(n)

            print(
                "OK",
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
        "完成",
        len(alive)
    )


if __name__=="__main__":
    main()
