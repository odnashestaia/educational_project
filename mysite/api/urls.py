from django.urls import path
from api.views import *
from rest_framework.authtoken import views as auth_views

urlpatterns = [
    path('products', products),
    path('products/<pk>', products_detal),
    path('token', auth_views.obtain_auth_token),
    path('cart', CartList.as_view()),
]