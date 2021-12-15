from django.urls import path
from . import views

app_name = 'cart_app'
urlpatterns = [
    path('', views.CartView.as_view()),
    path('queryAll/', views.CartListView.as_view(), name='queryAll'),
]
