from django.urls import path
from .views import UserCreateAPIView, UserListAPIView, UserUpdateAPIView, UserDestroyAPIView, UserRetreiveAPIView, UserAllDetailAPIView, UserDeactivateAPIView, UserActivateAPIView,UserChangePasswordAPIView

urlpatterns = [
    path('list/', UserListAPIView.as_view(), name='user-list'),
    path('create/', UserCreateAPIView.as_view(), name='user-create'),
    path('update/<slug:slug>/', UserUpdateAPIView.as_view(), name='user-update'),
    path('retreive<slug:slug>/', UserRetreiveAPIView.as_view(), name='user-retreive'),
    path('detail<slug:slug>/', UserAllDetailAPIView.as_view(), name='user-detail'),
    path('delete/<slug:slug>/', UserDestroyAPIView.as_view(), name='user-delete'),
    path('activate/<slug:slug>/', UserActivateAPIView.as_view(), name='user-activate'),
    path('deactivate/<slug:slug>/', UserDeactivateAPIView.as_view(), name='user-deactivate'),
    path('change-password/', UserChangePasswordAPIView.as_view(), name='user-change-password'),
]