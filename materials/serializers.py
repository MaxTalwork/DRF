from rest_framework.serializers import ModelSerializer, SerializerMethodField

from materials.models import Course, Lesson
from materials.validators import UrlValidator
from users.models import Subscription


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
