from flask import Flask

from database import init_db
import models
from database import db
from flask_restful import Api, Resource, abort, reqparse
from flask import jsonify
from sqlalchemy import desc
import json
import datetime

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    init_db(app)

    return app

app = create_app()

api = Api(app)

class Season(Resource):
    def get(self):
        try:
            api = []
            datas = db.session.query(models.Season).all()
            for season in datas:
                api.append({"id":season.id,"name":season.name})
            return jsonify(api)
        except:
            return { 'message': '500 error' }, 500

api.add_resource(Season, '/api/season')


class SeasonDetail(Resource):
    def get(self,name):
        api = []
        season = db.session.query(models.Season).filter(models.Season.name == name).first()
        try:
            if(season):
                api.append({"id":season.id,"name":season.name})
                return jsonify(api)
            return { 'message': '403 error' }, 403
        except:
            return { 'message': '500 error' }, 500

api.add_resource(SeasonDetail, '/api/season/name/<string:name>')

class SeasonDetailId(Resource):
    def get(self,id):
        api = []
        season = db.session.query(models.Season).filter(models.Season.id == id).first()
        try:
            if(season):
                api.append({"id":season.id,"name":season.name})
                return jsonify(api)
            return { 'message': '403 error' }, 403
        except:
            return { 'message': '500 error' }, 500

api.add_resource(SeasonDetailId, '/api/season/id/<int:id>')



class Article(Resource):
    def get(self):
        try:
            api = []
            parser = reqparse.RequestParser()
            parser.add_argument('limit', type=int)
            parser.add_argument('season_id', type=int)
            parser.add_argument('checkcount', type=str)
            query_data = parser.parse_args()
            
            datas = db.session.query(models.Article).all()
            
            if(query_data['limit'] and query_data['season_id'] and query_data['checkcount']):
                if(query_data['checkcount'] == "desc"):
                    datas = db.session.query(models.Article).filter(models.Article.season_id == query_data['season_id']).order_by(desc(models.Article.checkcount)).limit(query_data['limit']).all()
                elif(query_data['checkcount'] == "asc"):
                     datas = db.session.query(models.Article).filter(models.Article.season_id == query_data['season_id']).order_by(models.Article.checkcount).limit(query_data['limit']).all()
                else:
                   return { 'message': '403 error' }, 403
            elif(query_data['season_id'] and query_data['checkcount']):
                if(query_data['checkcount'] == "desc"):
                    datas = db.session.query(models.Article).filter(models.Article.season_id == query_data['season_id']).order_by(desc(models.Article.checkcount)).all()
                elif(query_data['checkcount'] == "asc"):
                    datas = db.session.query(models.Article).filter(models.Article.season_id == query_data['season_id']).order_by(models.Article.checkcount).all()
                else:
                   return { 'message': '403 error' }, 403
            elif(query_data['season_id']):
                datas = db.session.query(models.Article).filter(models.Article.season_id == query_data['season_id']).order_by(desc(models.Article.checkcount)).all()

            elif(query_data['limit'] and query_data['checkcount']):
                if(query_data['checkcount'] == "desc"):
                    datas = db.session.query(models.Article).order_by(desc(models.Article.checkcount)).limit(query_data['limit']).all()
                elif(query_data['checkcount'] == "asc"):
                    datas = db.session.query(models.Article).order_by(models.Article.checkcount).limit(query_data['limit']).all()
                else:
                    return { 'message': '403 error' }, 403
            elif(query_data['limit']):
                datas = db.session.query(models.Article).limit(query_data['limit']).all()
            elif(query_data['checkcount']):
                if(query_data['checkcount'] == "desc"):
                    datas = db.session.query(models.Article).order_by(desc(models.Article.checkcount)).all()
                elif(query_data['checkcount'] == "asc"):
                    datas = db.session.query(models.Article).order_by(models.Article.checkcount).all()
                else:
                    return { 'message': '403 error' }, 403

            for article in datas:
                api.append({"id":article.id,"season_id":article.season_id,"ttl":article.ttl,"detail":json.loads(article.detail),"synopsis":article.synopsis,"link":article.link,"checkcount":article.checkcount})
            return jsonify(api)
        except:
            return { 'message': '500 error' }, 500

api.add_resource(Article, '/api/article')


class ArticleDetail(Resource):
    def get(self,id):
        api = []
        article = db.session.query(models.Article).filter(models.Article.id == id).first()
        try:
            if(article):
                api.append({"id":article.id,"season_id":article.season_id,"ttl":article.ttl,"detail":json.loads(article.detail),"synopsis":article.synopsis,"link":article.link,"checkcount":article.checkcount})
                return jsonify(api)
            return { 'message': '403 error' }, 403
        except:
            return { 'message': '500 error' }, 500

api.add_resource(ArticleDetail, '/api/article/<int:id>')


