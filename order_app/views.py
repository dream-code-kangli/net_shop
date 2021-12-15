import uuid
from datetime import datetime

import jsonpickle
from django.db.models import F
from django.shortcuts import render, redirect, HttpResponse

from order_app.models import TradeOrder, TradeOrderItem
from user_app.models import Address
from net_shop_app.models import Inventory

# Create your views here.
from cart_app.cartmanager import DBCartManger


def toOrder(request):
    cartitems = request.GET.get('cartitems', '')
    totalPrice = request.GET.get('totalPrice', '')
    if not request.session.get('user'):
        return redirect('/user/login/?cartitems=' + cartitems + '&reflag=order' + '&totalPrice=' + totalPrice)

    cartItemList = jsonpickle.loads(cartitems)

    user = jsonpickle.loads(request.session.get('user', ''))
    address = user.address_set.filter(isdefault=True)
    if not address:
        return redirect('user_app:address')
    addrObj = user.address_set.get(isdefault=True)

    cartItemObjList = [DBCartManger(user).get_cartitems(**item) for item in cartItemList if item]
    return render(request, 'order_app/order.html',
                  {'totalPrice': totalPrice, 'cartItemObjList': cartItemObjList, 'addrObj': addrObj})


def pay(request):
    address = request.GET.get('address', -1)
    payway = request.GET.get('payway', 'alipay')
    cartitems = request.GET.get('cartitems', '')
    totalPrice = request.GET.get('totalPrice', '')

    user = jsonpickle.loads(request.session.get('user', ''))

    params = {
        'out_order_num': uuid.uuid4().hex,
        'order_num': datetime.now().strftime('%Y%m%d%H%M%S'),
        'address': Address.objects.get(id=address),
        'user': jsonpickle.loads(request.session.get('user', '')),
        'payway': payway
    }
    orderObj = TradeOrder.objects.create(**params)

    if cartitems:
        cartitems = jsonpickle.loads(cartitems)
        orderItemObj = [TradeOrderItem.objects.create(order=orderObj, **ci) for ci in cartitems if ci]

    orderObj.status = '待发货'
    orderObj.save()

    [Inventory.objects.filter(goods=orderItem.goodsid, color=orderItem.colorid, size=orderItem.sizeid).update(
        count=F('count') - orderItem.count) for orderItem in orderItemObj]

    [user.cartitem_set.filter(goodsid=orderItem.goodsid, colorid=orderItem.colorid, sizeid=orderItem.sizeid,
                              count=orderItem.count).delete() for orderItem in orderItemObj]
    orderObj = jsonpickle.dumps(orderObj)
    return redirect('/order/suPay/?orderObj='+orderObj+'&totalPrice='+totalPrice)


def supay(request):
    orderObj = request.GET.get('orderObj', '')
    orderObj = jsonpickle.loads(orderObj)
    totalPrice = request.GET.get('totalPrice', '')
    return render(request, 'order_app/pay.html', {'orderObj': orderObj, 'totalPrice': totalPrice})
