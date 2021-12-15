"""django_net_shop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.views.static import serve

from django_net_shop.settings import DEBUG, MEDIA_ROOT

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('net_shop_app.urls')),
    path('user/', include('user_app.urls')),
    path('cart/', include('cart_app.urls')),
    path('order/', include('order_app.urls')),
]

# if DEBUG:
#     urlpatterns += url(r'^media/(?P<path>.*)', serve, {'document_root': MEDIA_ROOT})


if DEBUG:
    urlpatterns += url(r'^media/(?P<path>.*)', serve, {'document_root': MEDIA_ROOT}),
