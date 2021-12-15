from django.urls import path
from . import views

app_name = 'user_app'
urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('center/', views.CenterView.as_view(), name='center'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('loadCode/', views.LoadCodeView.as_view(), name='loadCode'),
    path('checkCode/', views.CheckCode.as_view(), name='checkCode'),
    path('logout/', views.logout, name='logout'),
    path('address/', views.AddressView.as_view(), name='address'),
    path('loadArea/', views.loadAreaView),
    path('updateDefaultaddr/', views.updateDefaultaddr),

]
