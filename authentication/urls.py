from django.urls import path
from .views import CustomTokenObtainPairView, CustomRefreshView, CustomTokenBlacklistView

urlpatterns = [
    path('login/', CustomTokenObtainPairView.as_view(), name='login-user'),
    path('refresh/', CustomRefreshView.as_view(), name='refresh-token'),
    path('blacklist/', CustomTokenBlacklistView.as_view(), name='blacklist-token'),
    path('blacklist/', CustomTokenBlacklistView.as_view(), name='reset'),

]