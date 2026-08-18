import requests
import re
import random
import base64
import socket
from urllib.parse import urlparse


SOURCES = [
"https://raw.githubusercontent.com/zhuhaiuk/free-nodes/main/nodes.txt",
"https://raw.githubusercontent.com/mahdibland/V2RayAggregator/master/sub/sub_merge.txt",
"https://raw.githubusercontent.com/chengaopan/AutoMergePublicNodes/master/list.txt",
"https://raw.githubusercontent.com/free-nodes/v2rayfree/main/sub"
]


def download():

    result = ""

    for url in SOURCES:

        try:
            r = requests.get(url, timeout=15)

            if r.status_code == 200:
                result += "\n" + r.text

        except:
            pass

    return result



def extract_nodes(text):

    pattern = r"(?:vmess|vless|trojan|ss|ssr)://[^\s\"<>]+"

    return re.findall(pattern, text)



def get_host_port(node):

    try:

        if node.startswith("trojan://"):

            s = node.replace("trojan://","")
            hostport = s.split("@")[-1].split("?")[0]


        elif node.startswith("ss://"):

            s = node.split("@")[-1]
            hostport = s.split("#")[0]


        else:

            return None,None


        host = hostport.split(":")[0]
        port = int(hostport.split(":")[1])

        return host,port


    except:

        return None,None



def check_node(node):

    host,port = get_host_port(node)

    if not host:
        return True


    try:

        sock = socket.create_connection(
            (host,port),
            timeout=3
        )

        sock.close()

        return True


    except:

        return False



def main():

    data = download()

    nodes = extract_nodes(data)

    nodes = list(set(nodes))

    random.shuffle(nodes)


    alive=[]


    for n in nodes[:200]:

        if check_node(n):

            alive.append(n)


        if len(alive)>=50:

            break



    print("有效節點:",len(alive))



    with open(
        "nodes.txt",
        "w",
        encoding="utf-8"
    ) as f:

        for n in alive:

            f.write(n+"\n")



    sub = "\n".join(alive)


    sub64 = base64.b64encode(
        sub.encode("utf-8")
    ).decode("utf-8")



    with open(
        "sub.txt",
        "w",
        encoding="utf-8"
    ) as f:

        f.write(sub64)



if __name__=="__main__":

    main()
