from bs4 import BeautifulSoup
import requests

from sys import argv

printCountFreq = 30

def getIDfromHref(href):
    href = bytearray(href,'utf-8')
    pow = 1
    res = 0
    while(href[-1] != ord('Q')):
        res += (href[-1] - 48) * pow
        del href[-1]
        pow *=  10
    return res


def crawl(start):
    stack = []
    stack.append(start)
    visitedHrefs = set()
    count = 0
    while stack:
        if count == printCountFreq:
            print('Visited %d articles' % len(visitedHrefs))
            count = 0
        count += 1
        curr = stack.pop()
        print(f'Went into: {curr}')
        visitedHrefs.add(curr)
        html = requests.get(f'https://en.wikipedia.org{curr}').content.decode()
        soup = BeautifulSoup(html,'lxml')
        try:
            id = getIDfromHref(soup.find('li',{'id':'t-wikibase'}).a['href'])
        except AttributeError:
            print(f'AttributeError ocurred in: {curr}')
            continue
        if not id:
            print(f'Id not found in: {curr}')
            continue
        print(f'Article ID: {id}')
        for a in soup.findAll('a',href=True):
            href = a['href']
            if href in visitedHrefs:
                print(f'Omitting alredy visited {href}')
                continue
            if href[:6] == '/wiki/':
                stack.append(href)

try:
    start = argv[1]
except IndexError:
    start = '/wiki/Python_(programming_language)'
crawl(start)
