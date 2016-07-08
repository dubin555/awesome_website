# coding = utf-8

# Did not use the models from django.db
# from django.db import models

# Create your models here.
# Model from mongo
from mongoengine import Document
from mongoengine import connect
from mongoengine import *

# connect to mongodb
connect('ganji', host='127.0.0.1', port=27017)


class ItemInfo(Document):
    title = StringField()
    type = StringField()
    publish_time = StringField()
    price = IntField()
    area = StringField()
    meta = {'collection': 'item_info_with_type'}



def topx(dates, area, limit):

    pipeline = [
        {'$match': {'$and':[{'publish_time':{'$in':dates}},{'area':area}]}},
        {'$group':{'_id': "$type",'counts':{'$sum':1}}},
        {'$limit':limit},
        {'$sort':{'counts':-1}}
    ]
    for i in ItemInfo._get_collection().aggregate(pipeline):
        data = {
            'name': i['_id'],
            'data': [i['counts']],
            'type': 'column'
        }
        yield data

series_CP = [i for i in topx(['2016.06.02', '2016.06.07'], "昌平", 3)]
print(series_CP)


