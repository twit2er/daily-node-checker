import requests
import re
import random
import base64


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


    # 原始格式

    result += re.findall(
        r"(?:vmess|vless|trojan|ss|ssr)://[^\s\"<>]+",
        text
    )


    # base64訂閱

    if len(result)==0:

        d=decode_base64(text)

        result += re.findall(
            r"(?:vmess|vless|trojan|ss|ssr)://[^\s\"<>]+",
            d
        )


    return list(set(result))



def main():

    print("下載")

    data=download()


    nodes=extract(data)


    random.shuffle(nodes)


    print(
        "找到節點:",
        len(nodes)
    )


    # 暫時保存全部候選

    with open(
        "nodes.txt",
        "w",
        encoding="utf-8"
    ) as f:

        for n in nodes[:100]:

            f.write(
                n+"\n"
            )


    print(
        "保存候選:",
        min(100,len(nodes))
    )



if __name__=="__main__":

    main()
