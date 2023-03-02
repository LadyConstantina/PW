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
        help="Sends a get request to the url and shows the response")

    parser.add_argument(
        "-s",
        "--search",
        type = str,
        nargs='*',
        metavar="search path",
        default=None,
        help="Searches the data and shows frist 10 links"
    )

    args = parser.parse_args()

    if args.url != None:
        visit(args.url)
    if args.search != None:
        search(args.search)
        
def visit(url):
    webpage = VisitWeb.WebPage(url[0])
    resp,types = webpage.get_response()
    parser = Parse.Parser(resp,types)
    print(parser.get_resp())

def search(search):
    arguments = '+'.join(search)
    url1 = "https//www.google.com/search?q="+arguments+"&start=0"
    url2 = "https//www.google.com/search?q="+arguments+"&start=1"
    webpage1 = VisitWeb.WebPage(url1,print = False)
    webpage2 = VisitWeb.WebPage(url2,print = False)
    resp_1,type = webpage1.get_response()
    resp_2,type = webpage2.get_response()
    parser = Parse.Parser(resp_1,type)
    resp_1 = parser.get_links()
    parser = Parse.Parser(resp_2,type)
    resp_2 = parser.get_links()
    links = resp_1+resp_2
    for element in links:
        print(element)

if __name__ == "__main__":
    main()