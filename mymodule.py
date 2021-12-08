# coding: UTF-8
from urllib import request  # urllib.requestモジュールをインポート
from bs4 import BeautifulSoup
import re
import json
import models
from database import db
from app import app

url = "https://anime.eiga.com"

instance = request.urlopen(url+"/program/")

#パースする
soup = BeautifulSoup(instance,"html.parser")



def getAnimDl(el):
    obj = []
    for dt in el:
        obj.append({dt.text.strip(): dt.find_next("dd").text.strip()})
    return obj

def getDetailTxt(page,el):
    txt_one = page.select_one(el)
    if(txt_one):
        return txt_one.text
    else:
        return ""

def itemFunc(items,soup_list):
    headSeasonTtlL = soup_list.select_one(".headSeasonTtlL")
    season_id =""
    with app.app_context():
        season_id = db.session.query(models.Season).filter(models.Season.name == headSeasonTtlL.text).first().id
    for el in items:
        ttl = el.find("p",{"class":"seasonAnimeTtl"}).text
        link = re.findall(r'\d+',el.select_one(".seasonAnimeTtl > a").get("href"))

        seasonAnimeDetails = el.select("dl.seasonAnimeDetail > dt")
        dl_txt = json.dumps(getAnimDl(seasonAnimeDetails),indent=2,ensure_ascii=False)
        
        soup_detail = BeautifulSoup(request.urlopen(url + el.select_one(".seasonAnimeTtl > a").get("href")),"html.parser")
        detailLink = getDetailTxt(soup_detail,"#detailLink a")
        
        detailSynopsis = getDetailTxt(soup_detail,"#detailSynopsis > dd")
        detailMusic = getDetailTxt(soup_detail,"#detailMusic > dd")
        
        checkInCount = el.find("span",{"class":"checkInCountInner"}).text
        
        with app.app_context():
            article_data = db.session.query(models.Article).filter(models.Article.ttl == ttl).first()
            if(article_data):
                article_data.season_id = season_id
                article_data.detail = dl_txt
                article_data.synopsis = detailSynopsis
                article_data.music = detailMusic
                article_data.link = detailLink
                article_data.checkcount = checkInCount
                db.session.add(article_data)
                db.session.commit()
            else:
                new_season = models.Article(season_id=season_id,ttl=ttl,detail=dl_txt,synopsis=detailSynopsis,music=detailMusic,link=detailLink,checkcount=checkInCount)
                db.session.add(new_season)
                db.session.commit()

def optionFunc():
    for option_el in soup.select("#anime_term > option"):
        with app.app_context():
            if(not db.session.query(models.Season).filter(models.Season.name == option_el.text).all()):
                #データがあれば作成しない
                new_season = models.Season(name=option_el.text)
                db.session.add(new_season)
                db.session.commit()

def init():
    optionFunc()
    for option_el in soup.select("#anime_term > option"):
        # if(int(re.findall(r'\d+',option_el.text)[0]) <= 2016):
        soup_list = BeautifulSoup(request.urlopen(url + option_el["value"]),"html.parser")
        itemFunc(soup_list.select(".animeSeasonItemWrapper .animeSeasonBox"),soup_list)

    # items = soup.select(".animeSeasonItemWrapper .animeSeasonBox")
    # itemFunc(items,soup)