from django.urls import path
from .views import CustomTokenObtainPairView, CustomRefreshView, CustomTokenBlacklistView, userVerify

urlpatterns = [
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', CustomRefreshView.as_view(), name='token_refresh'),
    path('blacklist/', CustomTokenBlacklistView.as_view(), name='logout'),
    # path('blacklist/', CustomTokenBlacklistView.as_view(), name='reset'),
    #path('api/protected/' ,ProtectedView.as_view(), name='protected'),
    path('me/', userVerify.as_view(), name="me")
]