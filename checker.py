import requests
import re
import random


SOURCES = [

"https://raw.githubusercontent.com/zhuhaiuk/free-nodes/main/nodes.txt",

"https://raw.githubusercontent.com/mahdibland/V2RayAggregator/master/sub/sub_merge.txt",

"https://raw.githubusercontent.com/chengaopan/AutoMergePublicNodes/master/list.txt",

"https://raw.githubusercontent.com/ermaozi/get_subscribe/main/subscribe/clash.yml",

"https://cdn.jsdelivr.net/gh/vxiaov/free_proxies@main/clash/clash.provider.yaml",

"https://raw.githubusercontent.com/free-nodes/v2rayfree/main/sub",

"https://raw.githubusercontent.com/peasoft/NoMoreWalls/master/list.yml",

"https://raw.githubusercontent.com/ts-sf/fly/main/clash",

"https://raw.githubusercontent.com/ssrsub/ssr/master/singbox.json"

]


def download():

    result = ""

    for url in SOURCES:

        try:
            r = requests.get(
                url,
                timeout=15
            )

            if r.status_code == 200:
                result += "\n" + r.text

        except:
            pass

    return result



def extract(text):

    pattern = r"(vmess|vless|trojan|ss|ssr|hysteria2)://[^\s\"<>]+"

    nodes = re.findall(
        pattern,
        text
    )

    return nodes



def main():

    data = download()

    nodes = extract(data)

    nodes = list(set(nodes))

    random.shuffle(nodes)

    nodes = nodes[:50]


    with open(
        "nodes.txt",
        "w",
        encoding="utf-8"
    ) as f:

        for n in nodes:
            f.write(n+"\n")


    print(
        "节点数量:",
        len(nodes)
    )


if __name__ == "__main__":
    main()
