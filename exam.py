from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import config
from spider import Spider_Crawl



app = Flask(__name__)

app.config.from_object(config)

db = SQLAlchemy(app)

sp = Spider_Crawl()

url = "http://www.xbiquge.la/"

class Story(db.Model):
    __tablename__ = "story"
    id = db.Column(db.Integer, primary_key=True)
    #小说名
    name = db.Column(db.String(255))
    #小说的url
    url = db.Column(db.String(255))


class Story_Content(db.Model):
    __tablename__ = "story_content"
    id = db.Column(db.Integer, primary_key=True)
    #章节名
    list_name = db.Column(db.String(255))
    #章节名所对应的Url
    url = db.Column(db.String(255))
    #章节的实际内容
    list_content = db.Column(db.Text)
    #外键 关联是哪本小说的内容
    g_h = db.Column(db.ForeignKey(Story.id))


@app.route("/")
def index():
    html = sp.get_url(url)
    d = sp.parse(html)

    for key in d.keys():
        s = Story(name = key,url = d[key])
        db.session.add(s)
        db.session.commit()

    s_all = Story.query.all()
    return render_template("index.html",s_all = s_all)


@app.route("/detail_list/<id>")
def detail_list(id):
    s1 = Story.query.filter(Story.id==id).first()
    html = sp.get_url(s1.url)
    detail_d = sp.detail_parse(html)

    for key in detail_d:
        g_url = "http://www.xbiquge.la/" + detail_d[key]
        s_p = Story_Content(list_name = key,url = g_url,g_h = s1.id)
        db.session.add(s_p)
        db.session.commit()

    list_all = Story_Content.query.all()
    return render_template("detail_list.html", list_all=list_all)


@app.route("/detail_content/<id>")
def detail_content(id):
    detail = Story_Content.query.filter(Story_Content.id == id).first()
    title = detail.list_name
    print("----------------------------",title)
    html = sp.get_url(detail.url)
    content = sp.read_parse(html)
    print("这是我的第san个版本")
    return render_template("content.html", content = content,title = detail.list_name)

if __name__ == '__main__':
    db.drop_all()
    db.create_all()
    app.run(debug=True)

