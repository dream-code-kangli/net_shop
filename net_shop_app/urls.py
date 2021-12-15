from django.urls import path

from net_shop_app import views

app_name = 'good_app'
urlpatterns = [
    path('', views.IndexView.as_view()),
    path('category/<int:category_id>/', views.IndexView.as_view()),
    path('category/<int:category_id>/page/<int:num>/', views.IndexView.as_view()),
    path('goodsdetails/<int:good_id>/', views.DetailsView.as_view())

]

