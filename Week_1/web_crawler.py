import urllib
from sgmllib import SGMLParser

##############################################################################
class URLParser(SGMLParser):
    """ This class inherits SGMLParser and simply records to self.urls or
        self.text whenever a link is found or text is found, respectively. """

    def reset(self):
        SGMLParser.reset(self)
        self.urls = []
        self.text = []

    def start_a(self, attrs):
        href = [v for k, v in attrs if k=='href']
        if href:
            self.urls.extend(href)

    def handle_data(self, text):
        self.text.append(text)

##############################################################################
def find_urls(url):
    """ This function finds all the urls in a given page (returns a list). """
    try:
        sock = urllib.urlopen(url)
        parser = URLParser()
        #print sock.read()
        parser.feed(sock.read())
        sock.close()
        parser.close()
        return parser.urls
    except: # This is to take care of links that are not valid.
        return []

##############################################################################
def find_search_text(url, search_text):
    """ This function checks if the search text is in the text of the given
        page. """
    try:
        sock = urllib.urlopen(url)
        parser = URLParser()
        parser.feed(sock.read())
        sock.close()
        parser.close()
        for texts in parser.text:
            if search_text in texts:
                return True
        return False
    except: # This is to take care of links that are not valid.
        return False

##############################################################################
def find_urls_with_search_text(url, depth, search_text, urls_with_search_text):
    """ This recursive function crawls through all links on a given page and
        scans for a given level of depth. While crawling the function returns
        the url page containing the specified search text. """
    if depth <= 0:
        return

    if find_search_text(url, search_text) and url not in urls_with_search_text:
        urls_with_search_text.append(url)

    links = find_urls(url)
    for link in links:
        find_urls_with_search_text(link, depth-1, search_text, urls_with_search_text)

##############################################################################
if __name__ == "__main__":
    """ Example url, depth, and search_text
        Warning: This program may take a long time depending on the number of
        links in each page and the depth! """
    #url = 'http://jtsao22.wordpress.com'
    url = 'http://www.registrar.ucla.edu/schedule/detselect.aspx?termsel=12W&subareasel=EL+ENGR&idxcrs=0188++++'
    depth = 2
    #search_text = 'Found'
    #search_text = 'Closed'
    search_text = 'Open'
    urls_with_search_text = []

    find_urls_with_search_text(url, depth, search_text, urls_with_search_text);

    print urls_with_search_text
