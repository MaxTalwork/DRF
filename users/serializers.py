from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from users.models import Payment, User


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


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class SubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["email"]
