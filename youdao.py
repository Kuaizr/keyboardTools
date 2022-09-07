from importlib_metadata import re
import requests, json
import hashlib, time, random

def md5(word):
    #加密之前先进性编码
    word = word.encode()
    result = hashlib.md5(word)

    return result.hexdigest()


def youdao(word):
    '''
    这个函数用来实现发送请求(发送翻译的内容)得到翻译的数据
    :return:none
    '''
    url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'

    t = "4b1009b506fa4405f21e207abc4459fd"
    r = str(int(time.time()*1000))
    i = r + str(random.randint(0, 9))


    #字典类型的 words
    words = {
        'i': word,
        'from': 'AUTO',
        'to': 'AUTO',
        'smartresult': 'dict',
        'client': 'fanyideskweb',
        'salt': i,
        'sign': md5("fanyideskweb" + word + i + "Ygy_4c=r#e#4EX^NUGUc5"),
        'ts': r,
        'bv': 'd17d9dd026a611df0315b4863363408c',
        'doctype': 'json',
        'version': '2.1',
        'keyfrom': 'fanyi.web',
        'action': 'FY_BY_REALTlME',
    }
    #加请求头
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Length': '238',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': 'OUTFOX_SEARCH_USER_ID=-2102888696@10.108.160.17; JSESSIONID=aaaR36cnwMU_z_kMAgKjx; OUTFOX_SEARCH_USER_ID_NCOO=1730673226.5132544; ___rl__test__cookies=1590817621129',
        'Host': 'fanyi.youdao.com',
        'Origin': 'http://fanyi.youdao.com',
        'Referer': 'http://fanyi.youdao.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }
    result = requests.post(url, data=words, headers=headers)
    if json.loads(result.text)['errorCode'] != 0:
        return "something wrong"
    return json.loads(result.text)['translateResult'][0][0]["tgt"]

