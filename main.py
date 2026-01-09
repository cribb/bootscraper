import sys
from crawl import *

def main():    

    narg = len(sys.argv)

    if narg < 2:
        print("no website provided")
        sys.exit(1)
    elif narg > 2:
        print("too many arguments provided")
        sys.exit(1)

    script_name = sys.argv[0]
    url = sys.argv[1]
    print("Script name:", script_name)
    print("Argument: ", url)
    print("starting crawl of: ", url)
    html = get_html(url)
    print(html)
    sys.exit(0)



if __name__ == "__main__":
    main()
