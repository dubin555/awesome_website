from django.shortcuts import render, render_to_response
from django_web.models import ItemInfo
from django.core.paginator import Paginator
from django.template import RequestContext
import time
# Create your views here.

# Data Generator
# 区域发帖量前三名

def topx(date1, date2, area, limit):

    pipeline = [
        {'$match': {'$and':[{'publish_time':{'$gte': date1,'$lte': date2}},{'area': area}]}},
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

series_CP = [i for i in topx('2016.06.02', '2016.06.07', "昌平", 3)]
series_CY = [i for i in topx('2016.06.02', '2016.06.07', "朝阳", 3)]
series_HD = [i for i in topx('2016.06.02', '2016.06.07', "海淀", 3)]


# 发帖总量图
def total_post():
    pipeline = [
                {'$group':{'_id': "$type",'counts':{'$sum':1}}},
                {'$sort': {'counts': -1}},
                {'$limit': 15}
    ]
    for i in ItemInfo._get_collection().aggregate(pipeline):
        data = [
            i['_id'], i['counts']
        ]
        yield data
series_post = [i for i in total_post()]


# ================ Page View ==========================
def index(request, template_name="index.html"):
    limit = 15
    items = ItemInfo.objects
    paginatior = Paginator(items, limit)
    page = request.GET.get('page', 1)
    loaded = paginatior.page(page)

    # test_items = ItemInfo.objects[:10]
    return render(request, template_name, {"items": loaded})


def charts(request, template_name="chars.html"):
    context = {
        'chart_CP': series_CP,
        'chart_CY': series_CY,
        'chart_HD': series_HD,
        'chart_post': series_post
    }
    print("****", series_post)
    return render(request, template_name, context)


def page_not_found(request, template_name="page_404.html"):
    response = render_to_response(template_name, {}, context_instance=RequestContext(request))
    response.status_code = 404
    return response