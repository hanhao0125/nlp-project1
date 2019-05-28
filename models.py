from settings import db
from typing import Dict, List, Tuple
from config import BASE_SAVE_DIR
import pandas as pd
import numpy as np


class Content(db.Model):
    __tablename__ = "news_content"
    id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    content = db.Column(db.String(16), nullable=False, server_default="")

    def __repr__(self):
        return "<Content %r>" % self.id


def save_to_files(save_path: str = "news_content.csv") -> None:
    data = pd.read_sql_query("select * from news_content", db.engine)
    data.to_csv(BASE_SAVE_DIR + save_path, index=False)


def read_news_content(path: str = 'news_content.csv') -> pd.DataFrame:
    return pd.read_csv(BASE_SAVE_DIR + path)


def process_content() -> pd.DataFrame:
    d = read_news_content()

    return d

class WangYi(db.Model):
    __tablename__ = "wangyi"
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.Text, nullable=False, server_default="")
    content = db.Column(db.Text, nullable=False, server_default="")
    abstract = db.Column(db.Text, nullable=False, server_default="")

    date = db.Column(db.Text, nullable=False, server_default="")
    url = db.Column(db.Text, nullable=False, server_default="")
    comments = db.Column(db.Text, nullable=False, server_default="")
    heat = db.Column(db.Text, nullable=False, server_default="")

    def __repr__(self):
        return "<Content %r>" % self.id

if __name__ == "__main__":
    d = read_news_content()
    print(d.head())
    print(d.shape)
