import html2text

class Parser:
    def __init__(self,response,type):
        start = type.find(b'/') + 1
        self.type = type[start:start+4].decode().title()
        if self.type == "Html" or self.type == "Json" or self.type == "Plai":
            self.response = eval(self.type)(response)
        else:
            print("Unrecognised type of content or request problems")
            self.response = Plai(response)
    
    def get_resp(self):
        return self.response.get_resp()

    def get_links(self):
        return self.response.get_links()

class Html:
    def __init__(self,response):
        self.raw = response
        self.response = response

    def get_resp(self):
        return self.pretty(self.response)

    def get_links(self):
        return self.links()

    def pretty(self,resp):
        h = html2text.HTML2Text()
        h.body_width = 10000
        h.ignore_links = True
        return h.handle(resp.decode('latin-1'))

    def links(self):
        n = 0
        before = 0
        link = {}
        while n < 10:
            start = self.raw.find(b'<a href="/url?q=',before)+len(b'<a href="/url?q=')
            finish = self.raw.find(b'&',start)
            link[str(n)] = self.raw[start:finish]
            before = start
            n += 1
        return link
    
        

class Json:
    def __init__(self,response):
        self.raw = response
        self.response = response

    def get_resp(self):
        return self.pretty(self.response)

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
        return resp