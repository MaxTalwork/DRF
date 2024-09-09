from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView, get_object_or_404)
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from config.settings import EMAIL_HOST_USER
from materials.models import Course, Lesson
from materials.paginations import CustomPagination
from materials.serializers import (CourseDetailSerializer, CourseSerializer,
                                   LessonSerializer)
from users.models import Subscription
from users.permissions import IsModer, IsOwner
from rest_framework.decorators import action
from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework import status


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CourseDetailSerializer
        return CourseSerializer

    def perform_create(self, serializer):
        course = serializer.save(owner=self.request.user)
        course.save()

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (~IsModer,)
        elif self.action == "destroy":
            self.permission_classes = (~IsModer | IsOwner,)
        elif self.action in ["update", "retrieve"]:
            self.permission_classes = (IsModer | IsOwner,)
        return super().get_permissions()

    @action(detail=True, methods=("post",))
    def sub_update_email(self, request, pk):
        course = get_object_or_404(Course, pk=pk)
        serializer = self.get_serializer(course, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()

            subscriptions = Subscription.objects.filter(course=course)
            subscribers = [subscription.user for subscription in subscriptions]

            for subscriber in subscribers:
                send_mail(
                    "Подписка на курс",
                    f'Подписка на "{course.name}" была обновлеа',
                    EMAIL_HOST_USER,
                    [subscriber.email],
                    fail_silently=False,
                )

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LessonCreateApiView(CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (~IsModer, IsAuthenticated)

    def perform_create(self, serializer):
        lesson = serializer.save(owner=self.request.user)
        lesson.save()


class LessonListApiView(ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = CustomPagination


class LessonRetrieveAPIView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsModer | IsOwner)


class LessonDestroyAPIView(DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsOwner)


class LessonUpdateAPIView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsModer | IsOwner)
