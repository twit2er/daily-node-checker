import requests
import re
import random
import base64


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





def extract_full(text):


    pattern = r"(?:vmess|vless|trojan|ss|ssr|hysteria2)://[^\s\"<>]+"


    nodes = re.findall(
        pattern,
        text
    )


    return nodes





def main():


    data = download()


    nodes = extract_full(data)



    nodes = list(set(nodes))


    random.shuffle(nodes)



    nodes = nodes[:50]





    # 保存原始節點

    with open(
        "nodes.txt",
        "w",
        encoding="utf-8"
    ) as f:


        for n in nodes:

            f.write(
                n + "\n"
            )





    # 生成小火箭訂閱文件

    sub_content = "\n".join(nodes)



    sub_base64 = base64.b64encode(
        sub_content.encode("utf-8")
    ).decode("utf-8")



    with open(
        "sub.txt",
        "w",
        encoding="utf-8"
    ) as f:


        f.write(
            sub_base64
        )




    print(
        "節點數量:",
        len(nodes)
    )


    print(
        "sub.txt 已生成"
    )





if __name__ == "__main__":

    main()
