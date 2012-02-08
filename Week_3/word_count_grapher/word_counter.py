import urllib2
import operator
from sgmllib import SGMLParser

##############################################################################
class URLParser(SGMLParser):
    """ This class inherits SGMLParser and simply records to
        self.text whenever text is found. """

    def reset(self):
        SGMLParser.reset(self)
        self.text = []

    def handle_data(self, text):
        self.text.append(text)

    def get_words(self):
        return ''.join(self.text)


##############################################################################
def reduce_count(x, y):
    """ This function is the reduction function that accumulates the number of occurrences
        of a word """
    word, number = y.popitem()
    if word in x:
        x[word] += number
    else:
        x[word] = number
    return x

##############################################################################
def remove_articles(x):
    """ This function removes all articles """
    return x not in ['a', 'an', 'the', 'on', 'in', 'for', 'and', 'to']

##############################################################################
def parse_website(url):
    """ This function parses the website and returns the number of occurrences
        of every word in the page. """
    try:
        content = urllib2.urlopen(url).read()

        parser = URLParser()
        parser.feed(content)
        parser.close()
        all_words = parser.get_words().split()
        all_words_lower = map(lambda x: x.lower(), all_words)

        mapping = filter(remove_articles, all_words_lower)
        mapping = map(lambda x: {x: 1}, mapping)
        reduction = reduce(lambda x,y: reduce_count(x,y), mapping)

        return reduction
    except: # This is to take care of links that are not valid.
        return {}

##############################################################################
def get_top_10(word_counts):
    """ This functions gets the top 10 highest count words """
    return sorted(word_counts.iteritems(), key=operator.itemgetter(1))[-10:]

##############################################################################
def reduce_shortest(x,y):
    """ This is the reduce function for finding the shortest word """
    word, number = x.popitem()
    word2, number2 = y.popitem()
    if(number < number2):
        return {word: number}
    else:
        return {word2: number2}

##############################################################################
def reduce_longest(x,y):
    """ This is the reduce function for finding the longest word """
    word, number = x.popitem()
    word2, number2 = y.popitem()
    if(number > number2):
        return {word: number}
    else:
        return {word2: number2}

##############################################################################
def get_shortest_word(word_counts):
    """ This finds the shortest word in the word counts dictionary """
    mapping = map(lambda x: {x: len(x)}, word_counts)
    return reduce(lambda x,y: reduce_shortest(x,y), mapping)

##############################################################################
def get_longest_word(word_counts):
    """ This finds the longest word in the word counts dictionary """
    mapping = map(lambda x: {x: len(x)}, word_counts)
    return reduce(lambda x,y: reduce_longest(x,y), mapping)

##############################################################################
if __name__ == '__main__':
    url = "http://www.jtsao22.wordpress.com"
    word_counts = parse_website(url)
    print "Word Counts: " + str(word_counts)
    print "Top 10: " + str(get_top_10(word_counts))
    print "Shortest Word: " + str(get_shortest_word(word_counts))
    print "Longest Word: " + str(get_longest_word(word_counts))
