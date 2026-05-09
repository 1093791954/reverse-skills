"""
tls_curl_cffi_demo.py - 用 curl_cffi 模拟 Chrome JA3/JA4（教学 demo）
====================================================================
配套 SKILL.md Path 11。

curl_cffi 基于 libcurl-impersonate，能在 TLS 握手层完整模拟主流浏览器，
绕过 Akamai / DataDome / Cloudflare 的 JA3 检测。

依赖：
    pip install curl_cffi

合规边界：本脚本展示如何向"自有站点 / 测试 API"发起带 Chrome 指纹的请求；
不提供任何针对商业风控的封装。
"""

from curl_cffi import requests


def fetch_with_chrome131(url: str) -> str:
    """模拟 Chrome 131 的 TLS + HTTP/2 指纹。"""
    r = requests.get(url, impersonate="chrome131")
    return r.text[:500]


def fetch_with_safari(url: str) -> str:
    r = requests.get(url, impersonate="safari17_0")
    return r.text[:500]


def post_json(url: str, payload: dict) -> dict:
    r = requests.post(url, json=payload, impersonate="chrome131")
    return r.json()


if __name__ == "__main__":
    # 自检：访问公共 JA3 检测站点（记得用自己的 / 授权站点替换）
    # print(fetch_with_chrome131("https://tls.peet.ws/api/clean"))
    print("Available impersonates:")
    print("  chrome99 / chrome100 / chrome101 / chrome104 / chrome107 / chrome110 /")
    print("  chrome116 / chrome119 / chrome120 / chrome123 / chrome124 / chrome131 /")
    print("  edge99 / edge101 / safari15_3 / safari15_5 / safari17_0 / safari17_2_ios /")
    print("  firefox133 / firefox135")
