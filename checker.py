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

    result=""

    for url in SOURCES:

        try:

            r=requests.get(
                url,
                timeout=15
            )

            if r.status_code==200:

                result += "\n"+r.text


        except Exception:

            pass


    return result





def extract_nodes(text):

    pattern=r"(?:vmess|vless|trojan|ss|ssr)://[^\s\"<>]+"

    return re.findall(
        pattern,
        text
    )





def get_host_port(node):

    try:


        if node.startswith("trojan://"):

            s=node.replace(
                "trojan://",
                ""
            )

            hp=s.split("@")[-1].split("?")[0]



        elif node.startswith("ss://"):

            hp=node.split("@")[-1].split("#")[0]



        else:

            return None,None



        host=hp.split(":")[0]

        port=int(
            hp.split(":")[1]
        )


        return host,port



    except:

        return None,None






def tcp_test(node):


    host,port=get_host_port(node)


    if not host:

        return True



    try:


        s=socket.create_connection(
            (host,port),
            timeout=5
        )

        s.close()

        return True



    except:


        return False





def main():


    print("下載節點...")


    data=download()


    nodes=extract_nodes(data)


    nodes=list(set(nodes))


    random.shuffle(nodes)



    alive=[]



    print(
        "總節點:",
        len(nodes)
    )



    for n in nodes:


        if tcp_test(n):

            alive.append(n)

            print(
                "OK",
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



    text="\n".join(alive)



    encoded=base64.b64encode(
        text.encode()
    ).decode()



    with open(
        "sub.txt",
        "w",
        encoding="utf-8"
    ) as f:


        f.write(encoded)



if __name__=="__main__":

    main()
