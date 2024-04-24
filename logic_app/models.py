from django.db import models
from django.core.validators import MaxLengthValidator, MinLengthValidator, MaxValueValidator, MinValueValidator


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Excursion.StatusPublished.PUBLISHED)


class Validators:
    slug_validators = [
        MinLengthValidator(5, message="Минимум 5 символов"),
        MaxLengthValidator(60, message="Максимум 60 символов"),
    ]
    title_validators = slug_validators
    price_validators = [
        MinValueValidator(300, message="Минимальное значение цены 300"),
        MaxValueValidator(50000, message="Максимальное значение цены 50000")
    ]
    discount_validators = [
        MinValueValidator(10, message="Минимальное значение процента скидки 10"),
        MaxValueValidator(90, message="Максимальное значение процента скидки 90")
    ]


class Excursion(models.Model):
    class StatusPublished(models.IntegerChoices):
        DRAFT = False, "Черновик"
        PUBLISHED = True, "Опубликовано"

    title = models.CharField(max_length=75, verbose_name="Название Экскурсии", validators=Validators.title_validators)
    slug = models.SlugField(max_length=75, unique=True, db_index=True, verbose_name="Slug",
                            validators=Validators.slug_validators)
    price = models.IntegerField(verbose_name="Цена", validators=Validators.price_validators)
    discount = models.IntegerField(default=0, verbose_name="Скидка (%)",
                                   validators=Validators.discount_validators)
    header_photo = models.ImageField(upload_to="header_photo/", null=True, verbose_name="Заглавное фото экскурсии")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    is_published = models.BooleanField(choices=StatusPublished.choices, default=StatusPublished.DRAFT,
                                       verbose_name="Статус")
    category = models.ManyToManyField("Category", blank=True, related_name='excursion', verbose_name="Категории")
    location = models.ManyToManyField("Location", blank=True, related_name='excursion', verbose_name="Локации")

    objects = models.Manager()
    published = PublishedManager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Экскурсия"
        verbose_name_plural = "Экскурсии"


class Category(models.Model):
    title = models.CharField(max_length=75, verbose_name="Название Категории", validators=Validators.title_validators)
    slug = models.SlugField(max_length=75, unique=True, db_index=True, verbose_name="Slug",
                            validators=Validators.slug_validators)
    category_photo = models.ImageField(upload_to="category_photo/", null=True, blank=True,
                                       verbose_name="Заглавное фото категории")


class Location(models.Model):
    title = models.CharField(max_length=70, verbose_name="Название локации")
    short_info = models.TextField(blank=True, null=True, verbose_name="Короткое описание локации")
    location_photo = models.ImageField(upload_to="location_photo/", null=True, blank=True, verbose_name="Фото локации")
