from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from users.apps import UsersConfig
from users.views import (PaymentsCreateApiView, PaymentsDestroyAPIView,
                         PaymentsListApiView, PaymentsRetrieveAPIView,
                         PaymentsUpdateAPIView, SubscriptionAPIView,
                         UserViewSet)

app_name = UsersConfig.name

router = SimpleRouter()
router.register("", UserViewSet)
urlpatterns = [
    path(
        "login/",
        TokenObtainPairView.as_view(permission_classes=(AllowAny,)),
        name="token_obtain_pair",
    ),
    path(
        "token/refresh/",
        TokenRefreshView.as_view(permission_classes=(AllowAny,)),
        name="token_refresh",
    ),
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
    path("subscription/", SubscriptionAPIView.as_view(), name="subscription"),
]

urlpatterns += router.urls
