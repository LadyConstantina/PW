import socket

class WebPage:
    def __init__(self,address,print=True):
        self.print = print
        self.url = address
        self.type = b'none'
        self.response_body = self.visit()

    def get_response(self):
        return self.response_body, self.type

    def visit(self):
        start = self.url.find(b'//')
        finish = self.url.find(b'/',start+2)
        host = self.url[start+2:finish]
        req_path = self.url[finish:]
        HTTP_command = f"GET {req_path.decode()} HTTP/1.1 \r\nHost: {host.decode()}\r\nAccept: text/html; q=0.5, application/json; q=0.5\r\nConnection: keep-alive\r\n\r\n"
        if self.print: print("\n\nHTTP Request:\n\n",HTTP_command)
        HTTP_command = HTTP_command.encode()
        return self.send(HTTP_command,host)


    def send(self,request,host):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((socket.gethostbyname(host), 80))
        client.send(request)
        response = client.recv(2048)
        code = response[9:12]
        if code == b'200' or b'4' in code:
            new_line = response.find(b'\r\n\r\n')
            headers = response[:new_line]
            start = headers.find(b'Content-Type:')
            finish = headers.find(b'\r\n',start)
            self.type = headers[start+14:finish]
            contents = response[new_line:]
            if self.print: print("Initial response")
            if self.print: print("HTTP Response:\n\n",headers.decode(),"\n")
            if b'Content-Length:' in headers :
                start = response.find(b'Content-Length:')
                end = response.find(b'\r',start)
                content_length = int(response[start+16:end])
                response = self.fixed(client,content_length,contents)
            elif b'chunked' in headers:
                response = self.chuncked(client,contents[4:])
            return response
        elif b'3' in code:
            start = response.find(b'ocation: ') + len(b'ocation: ')
            end = response.find(b'\r\n',start)
            if self.url == response[start:end]:
                print("Can't handle redirections for https\n")
            else:
                print("Redirected to: ",self.url)
                resp = self.visit()

        if self.print: print(response.decode())
        return "None"

    def fixed(self,reader,length,content):
        reduce = len(content) - 4
        content += reader.recv(length-reduce)
        while len(content) < length:
            content += reader.recv(length-len(content))
        return content

    def chuncked(self,reader,content):
        if len(content) < 10:
            content += reader.recv(10)
        content, end_of_file = self.recursive_chunk(reader,content)
        end_of_file = False
        while not end_of_file:
            reader.recv(2)
            content_part, end_of_file = self.recursive_chunk(reader,b'')
            content += content_part
        return content
    
    def recursive_chunk(self,reader,content):
        content += reader.recv(10)
        start = content.find(b'\r\n')
        length = content[:start]
        length = int(length.decode(),16)
        if length == 0:
            return b'',True
        content = content[start+2:]
        much = len(content)
        content += reader.recv(length-much)
        while len(content) < length:
            content += reader.recv(length-len(content))
        return content,False