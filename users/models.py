from django.contrib.auth.models import AbstractUser
from django.db import models

from materials.models import Course


class User(AbstractUser):
    username = None
    email = models.EmailField(
        unique=True, verbose_name="Почта", help_text="Укажите почту"
    )
    phone = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        verbose_name="Телефон",
        help_text="Укажите телефон",
    )
    city = models.CharField(
        max_length=35,
        blank=True,
        null=True,
        verbose_name="Город",
        help_text="Укажите город",
    )
    avatar = models.ImageField(
        upload_to="users/avatars",
        verbose_name="Аватар",
        help_text="Разместите аватар",
        blank=True,
        null=True,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Payment(models.Model):
    payment_by = (("cash", "cash"), ("bank transfer", "bank transfer"))
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        verbose_name="Пользователь",
        max_length=150,
        help_text="Кто оплатил",
        blank=True,
        null=True,
    )
    payment_date = models.DateField(
        verbose_name="Дата оплаты", auto_now=True, help_text="Дата оплаты"
    )
    paid_for_course = models.CharField(
        "Course.name",
        max_length=150,
        help_text="За какой курс была оплата",
        blank=True,
        null=True,
    )
    paid_for_lesson = models.CharField(
        "Lesson.name",
        max_length=150,
        help_text="За какой урок была оплата",
        blank=True,
        null=True,
    )
    amount = models.PositiveIntegerField(
        verbose_name="Сумма оплаты",
        help_text="Укажите сумму оплаты",
    )
    payment_method = models.CharField(
        max_length=20,
        choices=payment_by,
        default="cash",
        verbose_name="Способ оплаты",
        help_text="Выбрать способ оплаты",
    )
    session_id = models.CharField(
        max_length=255,
        help_text="ID сессии",
        verbose_name="ID сессии",
        blank=True,
        null=True,
    )
    link = models.URLField(
        max_length=400,
        help_text="Ссылка на оплату",
        blank=True,
        null=True,
        verbose_name="Ссылка на оплату",
    )

    class Meta:
        verbose_name = "Платёж"
        verbose_name_plural = "Платежи"

    def __str__(self):
        return f"{self.user} оплатил курс(урок): {self.paid_for_course}({self.paid_for_lesson}) на сумму {self.amount}"


class Subscription(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        max_length=150,
        help_text="Кто подписан",
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name="Курс",
        max_length=150,
        help_text="На какой курс подписан",
    )
    is_subscribe = models.BooleanField(default=False, verbose_name="подписка")

    def __str__(self):
        return f"{self.user} подписан на курс: {self.course}"

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"


