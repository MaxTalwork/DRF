from rest_framework.serializers import ModelSerializer, SerializerMethodField

from materials.models import Course, Lesson, Subscription, Payment
from materials.validators import UrlValidator
from users.models import User


class CourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


class CourseDetailSerializer(ModelSerializer):
    lessons_in_course = SerializerMethodField()
    lessons_number = SerializerMethodField()

    def get_lessons_number(self, course):
        return Lesson.objects.filter(course=course).count()

    def get_lessons_in_course(self, course):
        return [lesson.name for lesson in Lesson.objects.filter(course=course)]

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return Subscription.objects.filter(user=user, course=obj).exists()
        return False

    class Meta:
        model = Course
        fields = "__all__"


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
        validators = [UrlValidator(field="link")]


class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = (
            "user",
            "payment_date",
            "paid_for_course",
            "paid_for_lesson",
            "amount",
            "payment_method",
        )


class SubscriptionSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ["email"]
