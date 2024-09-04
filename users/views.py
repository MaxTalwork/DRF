from rest_framework import filters
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView, get_object_or_404)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from materials.models import Course
from users.models import Payments, Subscription, User
from users.serializers import PaymentsSerializer, UserSerializer, SubscriptionSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class PaymentsCreateApiView(CreateAPIView):
    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer


class PaymentsListApiView(ListAPIView):
    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ("payment_date",)
    filterset_fields = ("paid_for_course", "paid_for_lesson", "payment_method")


class PaymentsRetrieveAPIView(RetrieveAPIView):
    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer


class PaymentsDestroyAPIView(DestroyAPIView):
    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer


class PaymentsUpdateAPIView(UpdateAPIView):
    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer


class SubscriptionAPIView(APIView):
    serializer_class = SubscriptionSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Subscription.objects.all()

    def post(self, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get("course")
        course_item = get_object_or_404(Course, pk=course_id)
        subs_item = Subscription.objects.filter(user=user, course=course_item)

        if subs_item.exists():
            subs_item.delete()
            message = "Подписка отключена"
        else:
            Subscription.objects.create(user=user, course=course_item)
            message = "Подписка включена"

        return Response({"message": message})
