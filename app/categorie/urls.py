from django.urls import path
from .views import CategoryCreateAPIView, CategoryListAPIView, CategorieUpdateAPIView, CategorieRetreiveAPIView, CategorieDeleteAPIView, CategorieDetailAPIView

urlpatterns =[
    path('list/', CategoryListAPIView.as_view(), name='category-list'),
    path('create/', CategoryCreateAPIView.as_view(), name='category-create'),
    path('update/<slug:slug>/', CategorieUpdateAPIView.as_view(), name='category-update'),
    path('delete/<slug:slug>/', CategorieDeleteAPIView.as_view(), name='category-delete'),
    path('retreive/<slug:slug>/', CategorieRetreiveAPIView.as_view(), name='category-retreive'),
    path('detail/<slug:slug>/', CategorieDetailAPIView.as_view(), name='category-detail'),
]
