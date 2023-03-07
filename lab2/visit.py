import argparse
import VisitWeb
import Parse

def main():
    parser = argparse.ArgumentParser(description = "go2web parser")
    parser.add_argument(
        "-u",
        "--url",
        type = str,
        nargs=1,
        metavar="url path",
        default=None,
        help="send a get request to the url and show the response")

    parser.add_argument(
        "-s",
        "--search",
        type = str,
        nargs='*',
        metavar="search words",
        default=None,
        help="search the data and show first 10 links"
    )

    args = parser.parse_args()

    if args.url != None:
        visit(args.url[0].encode('utf-8'))
    elif args.search != None:
        search(args.search)
        
def visit(url):
    webpage = VisitWeb.WebPage(url)
    resp,types = webpage.get_response()
    parser = Parse.Parser(resp,types)
    resp = parser.get_resp()
    print(resp)

def search(search):
    arguments = '+'.join(search)
    url1 = "https//www.google.com/search?q="+arguments
    webpage1 = VisitWeb.WebPage(url1.encode('utf-8'),print = False)
    resp_1,type = webpage1.get_response()
    parser = Parse.Parser(resp_1,type)
    resp = parser.get_links()
    for element in resp:
        print(element,":",resp[element].decode()[8:28])
    nr = 'a'
    while nr != 'q' :
        nr = input("Which link would you like to open? [quit with q] :")
        if nr >= '0' and nr <= '9':
            visit(resp[nr])
        elif nr == 'q':
            print("Bye!")
        else:
            print("Error: No link with such a number!")

if __name__ == "__main__":
    main()