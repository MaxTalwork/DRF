from django.urls import path
from rest_framework.routers import SimpleRouter

from users.apps import UsersConfig
from users.views import (PaymentsCreateApiView, PaymentsDestroyAPIView,
                         PaymentsListApiView, PaymentsRetrieveAPIView,
                         PaymentsUpdateAPIView, UserViewSet)

app_name = UsersConfig.name

router = SimpleRouter()
router.register("", UserViewSet)
urlpatterns = [
    path("payment/", PaymentsListApiView.as_view(), name="payment_list"),
    path(
        "payment/<int:pk>/", PaymentsRetrieveAPIView.as_view(), name="payment_retrieve"
    ),
    path("payment/create/", PaymentsCreateApiView.as_view(), name="payment_create"),
    path(
        "payment/<int:pk>/update/",
        PaymentsUpdateAPIView.as_view(),
        name="payment_update",
    ),
    path(
        "payment/<int:pk>/delete/",
        PaymentsDestroyAPIView.as_view(),
        name="payment_delete",
    ),
]

urlpatterns += router.urls
