from settings import app,db
import requests
from bs4 import BeautifulSoup
import re
from pprint import pprint as pp
from flask import render_template, request
from model import fetch
from models import WangYi as W
N = 100
def random_choose(n):
    return db.engine.execute(f"SELECT id,title FROM wangyi ORDER BY RANDOM() limit {n}")
    

@app.route('/n')
def fetch_news():
    news = random_choose(100)
    return render_template('main.html', n=news)



@app.route('/p')
def p():
    news_id = request.args.get('id')
    news = W.query.get(news_id)
    p = fetch(news.content)
    return render_template('p.html', c=news.title, p=p)


@app.route('/')
def page():
    return render_template('main.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port=11001)
