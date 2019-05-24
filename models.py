from settings import db
from typing import Dict, List, Tuple


class Content(db.Model):
    __tablename__ = "news_content"
    id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    content = db.Column(db.String(16), nullable=False, server_default="")

    def __repr__(self):
        return "<Content %r>" % self.id

def save_to_files(save_path: str = "123") -> None:
    with open("./news_content.txt", "w") as f:
        n = Content.query.all()
        for i in n:
            f.write(i.content)

def read_txt_files(path:str="./news_content.txt")->None:
    with open(path,'r') as f:
        for i in f.readlines():
            print(i)
if __name__ == "__main__":
    # save_to_files()
    read_txt_files()
    # print(Content.query.all())
