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
        # get url host uri
        start = self.url.find("//")
        finish = self.url.find("/",start+2)
        host = self.url[start+2:finish]
        # get additional arguments from url
        req_path = self.url[finish:]
        # write the HTTP request and encode it
        HTTP_command = f"GET {req_path} HTTP/1.1 \r\nHost: {host}\r\nAccept: text/html; q=0.5, application/json; q=0.5\r\n\r\n"
        if self.print: print("\n\nHTTP Request:\n\n",HTTP_command)
        HTTP_command = HTTP_command.encode()
        # Send the request and print it
        return self.send(HTTP_command,host)


    def send(self,request,host):
        # open a tcp socket and connect to the client
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((socket.gethostbyname(host), 80))
        # send request
        client.send(request)
        # read the first 2048 bytes of the response
        response = client.recv(2048)
        # get the status code
        code = response[9:12]
        # 200 -> succesful request
        if code == b'200':
            # find the delimeter (new line) between response headers and body
            new_line = response.find(b'\r\n\r\n')
            # get headers
            headers = response[:new_line]
            start = headers.find(b'Content-Type:')
            finish = headers.find(b'\r\n',start)
            self.type = headers[start+14:finish]
            # get body
            contents = response[new_line:]
            if self.print: print("Initial response")
            if self.print: print("HTTP Response:\n\n",headers.decode(),"\n") if self.print else print()
            # if there is a Content-Length: header, the response body has a fixed length
            if b'Content-Length:' in headers :
                # get the content length
                start = response.find(b'Content-Length:')
                end = response.find(b'\r',start)
                content_length = int(response[start+16:end])
                # read the response
                response = self.fixed(client,content_length,contents)
            # if there is no Content-Length: header, the response body is received in chuncks
            else:
                # read the response body
                response = self.chuncked(client,contents[4:])
            # return response
            return response
        if self.print: print(response)
        return "None"

    def fixed(self,reader,length,content):
        # get the length of already received body minus the new-line delimiter
        reduce = len(content) - 4
        # read more body of the expected length
        content += reader.recv(length-reduce)
        # if due some os reasons the received body is not of the expected length, read more bytes
        while len(content) < length:
            content += reader.recv(length-len(content))
        # return the decoded body
        return content

    def chuncked(self,reader,content):
        # to get the size of the first chunk we assure we have at least 10 bytes of the response body
        if len(content) < 10:
            content += reader.recv(10)
        # read the first chunck
        content, end_of_file = self.recursive_chunk(reader,content)
        end_of_file = False
        # untill we reach the end of response body (e.g. chunck of length 0)
        while not end_of_file:
            # ignore the '\r\n' delimeters between chunks
            reader.recv(2)
            # read a chunk
            content_part, end_of_file = self.recursive_chunk(reader,b'')
            # add it to the final response
            content += content_part
        #return the response body
        return content
    
    def recursive_chunk(self,reader,content):
        # read the first 10 bytes of the chunck for length retrieval
        content += reader.recv(10)
        # find the length of the chunck
        start = content.find(b'\r\n')
        length = content[:start]
        length = int(length.decode(),16)
        # if the chunck has length 0, we reached the end of the response body
        if length == 0:
            return b'',True
        # delete the delimiter '\r\n' between the length of chunck and the chunck itself
        content = content[start+2:]
        # get the length of the chunck we already read
        much = len(content)
        # read the remaining chunck of expected length
        content += reader.recv(length-much)
        # if due some os reasons the received body is not of the expected length, read more bytes
        while len(content) < length:
            content += reader.recv(length-len(content))
        # return the chunck and the status for end of file
        return content,False