from django.shortcuts import render, redirect

# Create your views here.
from django.views import View

from cart_app.cartmanager import getCartManger


class CartView(View):
    def post(self, request):
        # 在session中存取数据时使用到多级字典需要实时更新
        request.session.modified = True

        flag = request.POST.get('flag', '')
        if flag == 'add':
            CartManagerObj = getCartManger(request)
            CartManagerObj.add(**request.POST.dict())

        elif flag == 'plus':
            CartManagerObj = getCartManger(request)
            CartManagerObj.update(step=1, **request.POST.dict())

        elif flag == 'minus':
            CartManagerObj = getCartManger(request)
            CartManagerObj.update(step=-1, **request.POST.dict())

        elif flag == 'delete':
            CartManagerObj = getCartManger(request)
            CartManagerObj.delete(**request.POST.dict())

        return redirect('cart_app:queryAll')


class CartListView(View):
    def get(self, request):
        CartManagerObj = getCartManger(request)
        cartList = CartManagerObj.queryAll()

        return render(request, 'cart_app/cart.html', {'cartList': cartList})

