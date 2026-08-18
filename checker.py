import requests
import re
import random
import base64
import socket
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
            r = requests.get(
                url,
                timeout=15
            )

            if r.status_code == 200:
                text += "\n" + r.text

        except:
            pass

    return text



def decode(text):

    try:

        text += "=" * ((4-len(text)%4)%4)

        return base64.b64decode(
            text
        ).decode(
            errors="ignore"
        )

    except:

        return ""



def extract(text):

    nodes=[]


    nodes += re.findall(
        r"(?:vmess|vless|trojan|ss|ssr)://[^\s\"<>]+",
        text
    )


    if len(nodes)==0:

        d=decode(text)

        nodes += re.findall(
            r"(?:vmess|vless|trojan|ss|ssr)://[^\s\"<>]+",
            d
        )


    return list(set(nodes))



def port_check(node):

    try:

        if node.startswith("ss://"):

            host=node.split("@")[-1].split(":")[0]

            port=node.split("@")[-1].split(":")[1].split("#")[0]


        elif node.startswith("trojan://"):

            temp=node.replace(
                "trojan://",
                ""
            )

            host=temp.split("@")[-1].split(":")[0]

            port=temp.split("@")[-1].split(":")[1].split("?")[0]


        else:

            return True


        s=socket.create_connection(
            (
                host,
                int(port)
            ),
            timeout=3
        )

        s.close()

        return True


    except:

        return False



def main():

    print(
        "抓取節點"
    )


    data=download()

    nodes=extract(data)


    random.shuffle(nodes)


    print(
        "候選:",
        len(nodes)
    )


    alive=[]


    for n in nodes[:300]:


        if port_check(n):

            alive.append(n)

            print(
                "有效:",
                len(alive)
            )


        if len(alive)>=50:

            break



    print(
        "保存:",
        len(alive)
    )


    with open(
        "nodes.txt",
        "w",
        encoding="utf-8"
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
        encoding="utf-8"
    ) as f:

        f.write(sub)



if __name__=="__main__":

    main()
