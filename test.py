import requests
import subprocess
import json
import time
import os


def test_proxy(port):

    try:

        r = requests.get(
            "https://www.google.com",
            proxies={
                "http":
                f"socks5://127.0.0.1:{port}",
                "https":
                f"socks5://127.0.0.1:{port}"
            },
            timeout=8
        )

        if r.status_code == 200:
            return True


    except:
        pass


    return False



print(
    test_proxy(1080)
)
