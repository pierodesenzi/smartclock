import requests
from bs4 import BeautifulSoup


def estadao_internacional(): #html
    html = requests.get('https://internacional.estadao.com.br').content.decode()
    split_by_href = html.split('data-href', -1)
    formatted = []
    for t in split_by_href[1:]:
        link = t[2:].split('"')[0]
        title = t.split('data-title="')[1].split('">')[0]
        formatted.append({'source': 'O Estado de S. Paulo', 'link': link, 'title': title})
    return formatted

def globo_politica(): #rss feed
    raw = requests.get("https://g1.globo.com/rss/g1/politica/")
    xml = BeautifulSoup(raw.content, features='xml')

    articles = xml.findAll('item')
    article_list = []
    for a in articles:
        title = a.find('title').text
        link = a.find('link').text
        summary = a.find('description').text
        if 'img src' in summary:
            summary = summary.split('<br />')[1]
        article_list.append({
            'source': 'G1',
            'link': link,
            'title': title,
            'summary': summary
        })
        
    return article_list

def uol_reinaldo_azevedo(): #rss feed
    raw = requests.get("https://feeds.folha.uol.com.br/colunas/reinaldoazevedo/rss091.xml")
    xml = BeautifulSoup(raw.content, features='xml')

    articles = xml.findAll('item')
    article_list = []
    for a in articles:
        title = a.find('title').text
        link = a.find('link').text
        #summary = a.find('description').text
        #if 'img src' in summary:
        #    summary = summary.split('<br />')[1]
        article_list.append({
            'source': 'UOL - Reinaldo Azevedo',
            'link': link,
            'title': title,
            #'summary': summary
        })
        
    return article_list
