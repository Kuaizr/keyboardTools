from requests_toolbelt import MultipartEncoder
import requests, json, time
from clipboard import getClipBoardImg


class ImageBed:
    def __init__(self) -> None:
        self.host = "http://182.61.35.56:8090"
        self.admin_token = self.login()
        self.count = 0

    def login(self):
        '''这个函数用来实现登录功能，主要是得到Admin-Authorization'''
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Content-Length': '64',
            'Content-Type': 'application/json',
            'Host': '182.61.35.56:8090',
            'Origin': 'http://182.61.35.56:8090',
            'Pragma': 'no-cache',
            'Referer': 'http://182.61.35.56:8090/admin/index.html',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
        }

        url = self.host + "/api/admin/login"

        data = {
            "username": "kuaizhirui",
            "password": "Kzr100312",
        }
        result = requests.post(url, json=data, headers=headers)
        return json.loads(result.text)['data']['access_token']

    def getimglist(self):
        '''
        这个函数用来实现获取已经上传的图片列表
        :return:list
        '''
        url = self.host + 'api/admin/attachments'

        #加请求头
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Admin-Authorization': self.admin_token,
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Cookie': 'JSESSIONID=node0buyjqr31uy00x3iwid5x9zri179.node0',
            'Host': '182.61.35.56:8090',
            'Pragma': 'no-cache',
            'Referer': 'http://182.61.35.56:8090/admin/index.html',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
        }
        result = requests.get(url, headers=headers)
        print([  i['path'] for i in json.loads(result.text)['data']['content'] ])

    def pushimg(self):
        '''这个函数用来实现单张图片的上传，并得到markdown格式的文件'''
        url = self.host + "/api/admin/attachments/upload"
        imgdata = getClipBoardImg()
        filename = str(int(time.time() * 1000))+"."+imgdata[1]
        if imgdata[0] == "no img need to upload":
            return "no img need to upload"
        m = MultipartEncoder(
            fields = {
                "file":(filename,imgdata[0],'image/'+imgdata[1])
            }
        )
        headers = {
                'Accept': 'application/json, text/plain, */*',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Admin-Authorization': self.admin_token,
                'Cache-Control': 'no-cache',
                'Connection': 'keep-alive',
                'Content-Length': '20036',
                'Content-Type': m.content_type,
                'Host': '182.61.35.56:8090',
                'Origin': 'http://182.61.35.56:8090',
                'Pragma': 'no-cache',
                'Referer': 'http://182.61.35.56:8090/admin/index.html',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
            }
        result = requests.post(url,data=m, headers=headers)
        if json.loads(result.text)['status'] != 200:
            if self.count == 4:
                return("wrong")
            self.admin_token = self.login()
            self.pushimg()
            self.count = self.count + 1
        else:
            self.count = 0
            return self.markdownUrl(filename=filename,path=json.loads(result.text)['data']['path'])
        
    def markdownUrl(self,filename,path):
        return "!["+filename+"](" + path + ")"
