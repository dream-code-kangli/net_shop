import math

from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

# Create your views here.
from net_shop_app.models import Category, Goods, Color
from django.core.paginator import Paginator


class IndexView(View):
    def get(self, request, category_id=2, num=1):
        category_id = int(category_id)
        num = int(num)
        category_list = Category.objects.all().order_by('id')

        good_list = Goods.objects.filter(category_id=category_id).order_by('id')

        paginatorObj = Paginator(object_list=good_list, per_page=8)
        good_list_obj = paginatorObj.page(num)

        start = num - math.ceil(10 / 2)
        if start < 1:
            start = 1

        end = start + 9
        if end > paginatorObj.num_pages:
            end = paginatorObj.num_pages

        if end < 10:
            start = 1
        else:
            start = end - 9
        page_list = range(start, end + 1)

        return render(request, 'net_shop_app/index.html', {'category_list': category_list, 'good_list': good_list_obj,
                                                           'currentCid': category_id, 'page_list': page_list})


def recommend(func):
    def _wrapper(deteilsView, request, good_id, *args, **kwargs):
        # 获取cookie中的c_goods_id字符串
        c_goods_id = request.COOKIES.get('c_goods_id', '')

        # 存放用户访问过的商品ID
        goodsIdList = [int(id) for id in c_goods_id.split() if id.strip()]
        # 存放用户访问过的商品列表
        goodsObjList = [Goods.objects.get(id=gid) for gid in goodsIdList if
                        gid != good_id and Goods.objects.get(id=gid).category_id == Goods.objects.get(
                            id=good_id).category_id][:4]
        if good_id in goodsIdList:
            goodsIdList.remove(good_id)
            goodsIdList.insert(0, good_id)
        else:
            goodsIdList.insert(0, good_id)

        # 调用视图方法
        response = func(deteilsView, request, good_id, recommend_list=goodsObjList, *args, **kwargs)

        # 将用户访问过的商品ID列表存放到cookie中
        response.set_cookie('c_goods_id', ' '.join('%s' % id for id in goodsIdList), max_age=60 * 60)

        return response

    return _wrapper


class DetailsView(View):
    @recommend
    def get(self, request, good_id, recommend_list=[]):
        good_id = int(good_id)
        try:
            goods = Goods.objects.get(id=good_id)
            return render(request, 'net_shop_app/detail.html', {'goods': goods, 'recommend_list': recommend_list})
        except Goods.DoesNotExist:
            return HttpResponse(status=404)
