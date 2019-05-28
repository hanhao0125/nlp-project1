from gensim.models import KeyedVectors
from stanfordcorenlp import StanfordCoreNLP
from pprint import pprint as pp

base_path = '/root/files/'
file_path = base_path + 'news_content.csv'
nlp_path = '/root/stanford-corenlp'
word2vec_model_path = base_path + 'sgns.merge.word.bz2'
wm = KeyedVectors.load_word2vec_format(word2vec_model_path,
                                       binary=False,
                                       unicode_errors='ignore')
nlp = StanfordCoreNLP(nlp_path, lang='zh')


def search(query, depth=3):
    r = {}
    all_r = []
    topn = 10
    s = wm.most_similar(query, topn=topn)
    r[0] = {query: s}

    for d in range(1, depth):
        _v = r[d - 1]
        s = {}
        for k, v in _v.items():
            for i in v:
                s[i[0]] = wm.most_similar(i[0], topn=topn)
        r[d] = s
    for _, v in r.items():
        for _, k in v.items():
            all_r += k
    all_r = sorted(all_r, key=lambda x: x[1], reverse=True)
    all_r = set([i[0] for i in all_r])
    pp(all_r)
    return all_r


r = search('表示')
names = {'PERSON', 'ORGANIZATION'}
end = {'。', '!', '?'}
say_represents = r


def is_say(c):
    for i in say_represents:
        if i in c:
            return True
    return False


def find(s: str, return_mode: int = 1):
    '''
    @return_mode: 1. no filter; 2. have points
    '''
    points = []
    ners = nlp.ner(s)
    words = [i[0] for i in ners]
    k = 0
    while k < len(ners):
        if ners[k][1] in names:
            _p = [ners[k][0]]
            start = k
            while k < len(ners) and words[k] not in end: k += 1
            _p.append(''.join(words[start:k]))
            points.append(_p)
        k += 1
    points = list(filter(lambda x: is_say(x[1]), points))
    return points


def process_news(news):
    return news.replace('\n', '')


def fetch(news):
    n = process_news(news)
    p = find(n)
    return p
