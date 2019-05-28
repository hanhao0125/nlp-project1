from settings import app
import requests
from bs4 import BeautifulSoup
import re
from pprint import pprint as pp
from flask import render_template, request
from model import fetch


def get_news_content(url):
    return requests.get(url).content


def fetch_news_content(r):
    # test_url http://news.163.com/19/0527/08/EG5UJ7HF0001875P.html
    # r = get_news_content('http://news.163.com/19/0527/08/EG5UJ7HF0001875P.html')
    s = BeautifulSoup(r)
    t = s.find(class_=re.compile('post_text'))
    t = t.find_all('p', class_=False)
    c = ''
    for i in t:
        if 'style' in i.text or 'script' in i.text:
            continue
        c += i.text
    return c


def get_news():
    url = 'https://news.163.com/world/'
    soup = BeautifulSoup(get_news_content(url))
    a = soup.find_all(href=re.compile("news.163.com"), title=True, class_=False)
    links, title = [], []
    for i in a:
        links.append(i.get('href'))
        title.append(i.get('title'))
    c = []
    for l in links:
        c.append(fetch_news_content(get_news_content(l)))
    for i, j in zip(title, c):
        print(j)
    return {
        i: j for i, j in zip(title, c)
    }


news = get_news()


@app.route('/e')
def fetch_news():
    return render_template('main.html', n=list(news.keys()))


@app.route('/p')
def p():
    title = request.args.get('title')
    p = fetch(news[title])
    return render_template('p.html', c=news[title], p=p)


@app.route('/')
def page():
    return render_template('main.html')


if __name__ == '__main__':
    # fetch_news()
    app.run(debug=True, host='0.0.0.0')
