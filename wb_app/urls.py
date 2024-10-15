from django.urls import path
from .views import FetchProductInfo, ListProducts

urlpatterns = [
    path('fetch-product/', FetchProductInfo.as_view(), name='fetch-product'),
    path('list-products/', ListProducts.as_view(), name='list-products'),
]
