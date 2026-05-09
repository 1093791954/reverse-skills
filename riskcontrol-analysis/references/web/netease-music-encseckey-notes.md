# 网易云音乐 params + encSecKey - notes

## 摘要

网易云音乐 Web/H5/iOS Web 都用同一套 weapi/eapi 加密栈（古早但稳定）：

| 参数 | 含义 |
|---|---|
| `params` | AES-CBC 加密 body（base64） |
| `encSecKey` | RSA 加密 AES key（hex） |
| `csrf_token` | 评论/发布等接口必带 |

**算法**（公开多年）：
```
i = randstr(16)
encText = AES_CBC(text, "0CoJUm6Qyw8W8jud", "0102030405060708")  # 第一层
encText = AES_CBC(encText, i, "0102030405060708")                  # 第二层
encSecKey = RSA(reverse(i), pubKey, modulus)
params = base64(encText)
```

固定常量：第一层 key = `"0CoJUm6Qyw8W8jud"`、IV = `"0102030405060708"`、modulus = `010001`、pubKey 是 256 字节常量。

## 识别签名

- POST body 同时含 `params` 和 `encSecKey`。
- 接口路径 `/weapi/...`、`/api/...`、`/eapi/...`。
- pubKey/modulus 是公开固定值，全网一样。

## 还原方法

直接抄常量，用 Python `pycryptodome` 三行代码搞定，没难度：

```python
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
import base64, secrets

def weapi(text):
    PRESET_KEY = b"0CoJUm6Qyw8W8jud"
    IV = b"0102030405060708"
    PUBKEY = "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"
    MODULUS = "010001"

    i = secrets.token_urlsafe(12)[:16].encode()
    e1 = AES.new(PRESET_KEY, AES.MODE_CBC, IV).encrypt(pad(text.encode()))
    e1 = base64.b64encode(e1)
    e2 = AES.new(i, AES.MODE_CBC, IV).encrypt(pad(e1))
    params = base64.b64encode(e2).decode()

    rev_i = i[::-1].hex()
    encSecKey = pow(int(rev_i, 16), int(MODULUS, 16), int(PUBKEY, 16))
    encSecKey = format(encSecKey, '0256x')

    return {"params": params, "encSecKey": encSecKey}
```

## raw-hits 来源

- 见 [raw-hits/android-batch1.md Q10](../raw-hits/android-batch1.md)。

## 关键 URL

入门：
- [params 与 encSecKey 参数逆向 (CSDN 2025-08)](https://blog.csdn.net/chuanl5949/article/details/149885558)
- [网易云搜索接口 JS 逆向 (阿里云开发者 2024-08)](https://developer.aliyun.com/article/1596740)

进阶：
- [JS 逆向之网易云参数 (掘金)](https://juejin.cn/post/7023252269952925733)

公开仓库：
- [Binaryify/NeteaseCloudMusicApi (Node.js 完整 API)](https://github.com/Binaryify/NeteaseCloudMusicApi)
- [golangboy/wangyiyuncore (核心加密 JS 整合)](https://github.com/golangboy/wangyiyuncore)

## 工作流建议

入门 Skill 用例，5 分钟搞定：抄常量、写 weapi 函数、跑通即可。适合作为"风控参数还原 hello world"。
