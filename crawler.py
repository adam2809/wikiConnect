from bs4 import BeautifulSoup
import requests

# https://en.wikipedia.org/wiki?curid=
visitedHrefs = set()
# toExclude = (('/Special:BookSources/',3),
#              (3),
#              (3))
toExclude = ['Template:','Template_talk:','Category:',
             'Wikipedia:','Special:','Help:',
             'Portal:',]

def getIDfromHref(href):
    href = bytearray(href,'utf-8')
    pow = 1
    res = 0
    while(href[-1] != ord('Q')):
        res += (href[-1] - 48) * pow
        del href[-1]
        pow *=  10
    return res


def isValidArticleHref(href):
    if href[:6]!='/wiki/' or ':' in href:
        return False
    return True



def crawl(href):
    print(f'Went into: {href}')
    visitedHrefs.add(href)
    html = requests.get(f'https://en.wikipedia.org{href}').content.decode()
    soup = BeautifulSoup(html,'lxml')
    try:
        id = getIDfromHref(soup.find('li',{'id':'t-wikibase'}).a['href'])
    except AttributeError:
        print(f'AttributeError ocurred in: {href}')
        return
    if not id:
        print(f'Id not found in: {href}')
        return
    print(f'Article ID: {id}')
    for a in soup.findAll('a',href=True):
        link = a['href']
        if link in visitedHrefs:
            print(f'Omitting alredy visited {link}')
            continue
        if link[:6] == '/wiki/':
            crawl(link)


crawl('/wiki/Adolf_Hitler')
