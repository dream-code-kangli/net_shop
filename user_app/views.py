import jsonpickle
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse

# Create your views here.
from django.views import View

from cart_app.cartmanager import SessionCartManager
from order_app.models import TradeOrder
from user_app.models import UserInfo, Area, Address
from utils.code import gene_code
from django.core.serializers import serialize


class RegisterView(View):
    def get(self, request):
        return render(request, 'user_app/register.html')

    def post(self, request):
        uname = request.POST.get('account', '')
        password = request.POST.get('password', '')
        try:
            user = UserInfo.objects.get(uname=uname, pwd=password)
            return HttpResponse('该用户已存在')
        except UserInfo.DoesNotExist:
            user = UserInfo.objects.create(uname=uname, pwd=password)
            request.session['user'] = jsonpickle.dumps(user)
        return redirect('user_app:center')


class CenterView(View):
    def get(self, request):
        if request.session.get('user', ''):
            user = jsonpickle.loads(request.session.get('user', ''))
            num = TradeOrder.objects.filter(user_id=user.id).filter(status='待发货').count()
        return render(request, 'user_app/center.html', {'num': num})


class LoginView(View):
    def get(self, request):
        reflag = request.GET.get('reflag', '')
        cartitems = request.GET.get('cartitems', '')
        totalPrice = request.GET.get('totalPrice', '')
        return render(request, 'user_app/login.html',
                      {'reflag': reflag, 'cartitems': cartitems, 'totalPrice': totalPrice})

    def post(self, request):
        uname = request.POST.get('account', '')
        pwd = request.POST.get('password', '')

        reflag = request.POST.get('reflag', '')
        cartitems = request.POST.get('cartitems', '')
        totalPrice = request.POST.get('totalPrice', '')

        user = UserInfo.objects.filter(uname=uname, pwd=pwd)
        if user:
            request.session['user'] = jsonpickle.dumps(user[0])

            # 将session中的数据存储到数据库中
            SessionCartManager(request.session).migrateSession2DB()
            if reflag == 'cart':
                return redirect('cart_app:queryAll')

            elif reflag == 'order':
                return redirect('/order/?cartitems=' + cartitems + '&totalPrice=' + totalPrice)
            return redirect('user_app:center')
        return redirect('user_app:register')


class LoadCodeView(View):
    def get(self, request):
        img, code = gene_code()
        request.session['code'] = code
        return HttpResponse(img, content_type='image/png')


class CheckCode(View):
    def get(self, request):
        session_code = request.session.get('code', -1)
        code = request.GET.get('code', -2)

        vFlag = False
        if code == session_code:
            vFlag = True

        return JsonResponse({'vFlag': vFlag})


def logout(request):
    if request.session['user']:
        del request.session['user']
    return JsonResponse({'logout': True})


class AddressView(View):
    def get(self, request):
        user = request.session.get('user')
        if user:
            user = jsonpickle.loads(user)
        addr_list = user.address_set.all()
        return render(request, 'user_app/address.html', {'addr_list': addr_list})

    def post(self, request):
        aname = request.POST.get('aname', '')
        aphone = request.POST.get('aphone', '')
        addr = request.POST.get('addr', '')

        user = request.session.get('user')
        if user:
            user = jsonpickle.loads(user)
        Address.objects.create(aname=aname, aphone=aphone, addr=addr, userInfo=user,
                               isdefault=(lambda count: True if count == 0 else False)(user.address_set.count()))
        return redirect('user_app:address')


def loadAreaView(request):
    pid = request.GET.get('pid', -1)
    pid = int(pid)

    areaList = Area.objects.filter(parentid=pid)
    jareaList = serialize('json', areaList)

    return JsonResponse({'jareaList': jareaList})


def updateDefaultaddr(request):
    addrid = request.GET.get('addrid')
    addrid = int(addrid)

    Address.objects.filter(id=addrid).update(isdefault=True)
    Address.objects.exclude(id=addrid).update(isdefault=False)

    return redirect('user_app:address')
