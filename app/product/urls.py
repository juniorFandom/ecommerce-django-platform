from django.urls import path
from .views import (ProductCreateAPIView, ProductListAPIView, ProductUpdateAPIView, ProductDeleteAPIView)

urlpatterns = [
    path('list/', ProductListAPIView.as_view(), name='product-list'),
    path('create/', ProductCreateAPIView.as_view(), name='product-create'),
    path('update/<slug:slug>/', ProductUpdateAPIView.as_view(), name='product-update'),
    path('delete/<slug:slug>/', ProductDeleteAPIView.as_view(), name='product-delete'),
]