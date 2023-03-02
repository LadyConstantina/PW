import json
from bs4 import BeautifulSoup

class Parser:
    def __init__(self,response,type):
        start = type.find(b'/') + 1
        self.type = type[start:start+4].decode().title()
        self.response = eval(self.type)(response)
    
    def get_resp(self):
        return self.response.get_resp()

    def get_links(self):
        return self.response.get_links()

class Html:
    def __init__(self,response):
        self.raw = response
        self.response = self.pretty(response)

    def get_resp(self):
        return self.response

    def get_links(self):
        return self.links()

    def pretty(self,resp):
        soup = BeautifulSoup(resp,"html5lib")
        return soup.text

    def links(self):
        n = 9
        before = 0
        link = []
        while n > 0:
            start = self.raw.find(b'<a href="/url?q=',before)+len(b'<a href="/url?q=')
            finish = self.raw.find(b'"',start)
            link.append(self.raw[start:finish].decode()+"\n")
            before = start
            n -= 1
        return link
    
        

class Json:
    def __init__(self,response):
        self.raw = response
        self.response = self.pretty(response)

    def get_resp(self):
        return self.response

    def get_links(self):
        return self.raw

    def pretty(self,resp):
        return resp.decode().replace("{","").replace("}","").replace("\r\n","").replace(",","").replace("\"","").replace(":"," ->")

class Plai:
    def __init__(self,response):
        self.response = self.pretty(response)

    def get_resp(self):
        return self.response

    def pretty(self,resp):
        return resp.decode()