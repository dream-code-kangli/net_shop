from django.urls import path
from . import views

app_name = 'order_app'
urlpatterns = [
    path('', views.toOrder, name='order'),
    path('pay/', views.pay),
    path('suPay/', views.supay, name='suPay'),
]
