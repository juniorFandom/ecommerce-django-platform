from django.urls import path

from .views import (
    CreateCommandeAPIView,
    ListCommandeAPIView,
    RetrieveCommandeAPIView,
    UpdateCommandeAPIView,
    DeleteCommandeAPIView,
)

urlpatterns = [
    path(
        "",
        ListCommandeAPIView.as_view(),
        name="commande-list"
    ),

    path(
        "create/",
        CreateCommandeAPIView.as_view(),
        name="commande-create"
    ),

    path(
        "<slug:slug>/",
        RetrieveCommandeAPIView.as_view(),
        name="commande-detail"
    ),

    path(
        "<slug:slug>/update/",
        UpdateCommandeAPIView.as_view(),
        name="commande-update"
    ),

    path(
        "<slug:slug>/delete/",
        DeleteCommandeAPIView.as_view(),
        name="commande-delete"
    ),
]