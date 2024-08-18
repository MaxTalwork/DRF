from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название курса")
    preview = models.ImageField(
        upload_to="materials/preview",
        verbose_name="Изображение",
        help_text="Загрузите картинку",
        blank=True,
        null=True,
    )
    description = models.TextField(blank=True, null=True, help_text="Описание")

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название урока")
    description = models.TextField(blank=True, null=True, help_text="Описание урока")
    preview = models.ImageField(
        upload_to="materials/preview",
        verbose_name="Изображение",
        help_text="Загрузите картинку",
        blank=True,
        null=True,
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        verbose_name="Курс",
        help_text="К какому курсу относится урок",
        blank=True,
        null=True,
    )
    link = models.URLField(
        blank=True,
        null=True,
        verbose_name="Ссылка на выидео",
        help_text="Ссылка на выидео",
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
