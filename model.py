from __future__ import print_function, unicode_literals
from gensim.models import KeyedVectors
from stanfordcorenlp import StanfordCoreNLP
from pyltp import NamedEntityRecognizer,Postagger,Segmentor
from pprint import pprint as pp
import pickle as pkl
base_path = '/root/files/'
file_path = base_path + 'news_content.csv'
nlp_path = '/root/stanford-corenlp'
word2vec_model_path = base_path + 'sgns.merge.word.bz2'

segmentor = Segmentor()
segmentor.load('/root/files/ltp_data_v3.4.0/cws.model')
postagger = Postagger()
postagger.load('/root/files/ltp_data_v3.4.0/pos.model')
recongnizer = NamedEntityRecognizer()
recongnizer.load('/root/files/ltp_data_v3.4.0/ner.model')

r = None
with open('./saved_files/r.pkl','rb') as f:
    r = pkl.load(f)

end = {'。','!','?'}
say_represents = r
update = {'的','和','但','是','也'}
say_represents = say_represents - update
# convert ltp to bosonnlp foramt: {'word':words,'entity':[[start,end,org_name]]}
def ltp_ner(news):
    mapper = {'Ni':'org_name','Nh':'person_name'}
    words = segmentor.segment(news)
    postags = postagger.postag(words)
    nertags = recongnizer.recognize(words,postags)
    entity = []
    k = 0
    while k < len(words):
        if nertags[k] == 'O' or nertags[k].endswith('Ns'):
            k += 1
        elif nertags[k].startswith('S'):
            entity.append([k,k+1,mapper[nertags[k][2:]]])
            k += 1
        elif nertags[k].startswith('B'):
            start = k
            while k < len(words) and not nertags[k].startswith('E'):k+=1
            entity.append([start,k+1,mapper[nertags[k][2:]]])
            k += 1
        else:
            k += 1
    return {
        'word':list(words),
        'entity':entity
    }

# search the related keywords that can represens 说.
# alreadly saved to saved_files/r.pkl
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


def contains_say_keywords(c):
    return any(True if i in c else False for i in say_represents)


def all_say_keywords(c):
    return [i for i in c if i in say_represents]


# find the most nearest entity, and update the points. TODO: bad implements, need refactor. 
def correct_p(p):
    # currectly fetch the first keyword
    k_index = p[1].find(p[2][0])
    e_index = p[1].find(p[0])
    ner = uniteNER(p[1])
    e = ner[1]
    ret = p[0]
    clost = k_index - e_index - 1
    for start,end in e.items():
        if k_index < end:
            continue
        if (k_index - end) < clost:
            # update
            ret = ner[2][start:end]
            clost = k_index - end
    return [''.join(ret),p[1],p[2]]


# uniteNER, currently use the ltp as backend.
def uniteNER(news):
    ner = ltp_ner(news)
    words = ner['word']
    entity = ner['entity']
    N = []
    # record the entity start and end. k:v = start : end
    entity_start = {}
    for e in entity:
        if e[2] in {'org_name','person_name'}:
            entity_start[e[0]] = e[1]
            N.append([''.join(words[e[0]:e[1]]),e[2]])
    return N, entity_start, words


def bosonnlpNER(news):
    from bosonnlp import BosonNLP
    nlp = BosonNLP('cKWUytiR.34676.f5F2YbS_EyX2')
    ner = nlp.ner(news)[0]
    print(ner)
    words = ner['word']
    entity = ner['entity']
    N = []
    # record the entity start and end. k:v = start : end
    entity_start = {}
    for e in entity:
        if e[2] in {'org_name','person_name'}:
            entity_start[e[0]] = e[1]
            N.append([''.join(words[e[0]:e[1]]),e[2]])
    return N, entity_start, words


def extract_points(news,correct=False):
    points = []
    ners, es, words = uniteNER(news)
    k = 0
    while k < len(words):
        if k in es:
            # entity start, fetch the sentence
            # first add the entity
            _p = [''.join(words[k:es[k]])]
            # second add the sentence
            start = k
            # find the finish signal
            while k < len(words) and words[k] not in end:k+=1
            _p.append(words[start:k])
            
            points.append(_p)
        k += 1
    # filter the none points sentences. 
    # currently methods is naive: filter the sentence by keywords which can represent says
    points = list(filter(lambda x: contains_say_keywords(x[1]),points))
    keywords = [all_say_keywords(p[1]) for p in points]
    points = [[i[0],''.join(i[1]),k] for i,k in zip(points,keywords)]
    if correct:
        points = [correct_p(i) for i in points]
    return points


def process_news(news):
    return news.replace('\n', '')


def fetch(news):
    n = process_news(news)
    return extract_points(n),extract_points(n,correct=True) 
