from django.urls import path
from .views import (ProductCreateAPIView, ProductListAPIView, ProductUpdateAPIView, ProductDeleteAPIView)

urlpatterns = [
    path('products/', ProductListAPIView.as_view(), name='product-list'),
    path('products/create/', ProductCreateAPIView.as_view(), name='product-create'),
    path('products/<slug:slug>/update/', ProductUpdateAPIView.as_view(), name='product-update'),
    path('products/<slug:slug>/delete/', ProductDeleteAPIView.as_view(), name='product-delete'),
]