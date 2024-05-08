from django.db import models
from django.core.validators import MaxLengthValidator, MinLengthValidator, MaxValueValidator, MinValueValidator
from django.db.models import Count
from django.urls import reverse_lazy
from pytils.translit import slugify


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().annotate(location_count=Count('location__id')).filter(is_published=True)


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
        MinValueValidator(0, message="Минимальное значение процента скидки 0"),
        MaxValueValidator(90, message="Максимальное значение процента скидки 90")
    ]
    duration_validators = [
        MinValueValidator(1, message="Минимальное значение продолжительности экскурсии"),
        MaxValueValidator(24, message="Максимальное значение продолжительности экскурсии"),
    ]


class Excursion(models.Model):
    status_published = {
        False: "В Черновике",
        True: "Опубликована"
    }
    choices_discount = {
        v: f"{v} Процентов" if v != 0 else "Без скидки" for v in range(0, 91, 5)
    }
    excursion_top = {
        False: "Нет",
        True: "Да",
    }

    title = models.CharField(max_length=75, verbose_name="Название Экскурсии", validators=Validators.title_validators)
    slug = models.SlugField(max_length=75, unique=True, db_index=True, verbose_name="Slug",
                            validators=Validators.slug_validators)
    duration = models.FloatField(verbose_name="Продолжительность экскурсии", default=1,
                                 validators=Validators.duration_validators)
    geo = models.CharField(max_length=35, verbose_name="Гео экскурсии", default="Сочи-Адлер")
    price = models.IntegerField(verbose_name="Цена", validators=Validators.price_validators)
    discount = models.IntegerField(default=0, verbose_name="Скидка (%)",
                                   validators=Validators.discount_validators, choices=choices_discount)
    header_photo = models.ImageField(upload_to="header_photo/", blank=True, null=True,
                                     verbose_name="Заглавное фото экскурсии")
    description = models.TextField(blank=True, null=True, verbose_name="Описание экскурсии")
    is_published = models.BooleanField(choices=status_published,
                                       default=False,
                                       verbose_name="Статус")
    top = models.BooleanField(choices=excursion_top, default=False,
                              verbose_name="Отображение экскурсии на главной странице")
    category = models.ManyToManyField("Category", blank=True, related_name='excursion', verbose_name="Категории")
    location = models.ManyToManyField("Location", blank=True, related_name='excursion', verbose_name="Локации")

    objects = models.Manager()
    published = PublishedManager()

    @classmethod
    def get_tours_with_count_location(cls):
        return cls.objects.annotate(location_count=Count('location__id')).filter(is_published=True, top=True)

    @classmethod
    def get_tour_with_locations_by_slug(cls, slug: str):
        return cls.objects.prefetch_related('location').filter(slug=slug)

    @classmethod
    def get_tours_by_category_slug(cls, slug: str):
        return cls.objects.annotate(location_count=Count('location__id')).filter(is_published=True, category__slug=slug)

    def get_absolute_url(self):
        return reverse_lazy('excursion', kwargs={"excursion_slug": self.slug})

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Экскурсию"
        verbose_name_plural = "Экскурсии"


class Category(models.Model):
    title = models.CharField(max_length=75, verbose_name="Название Категории", validators=Validators.title_validators)
    slug = models.SlugField(max_length=75, unique=True, db_index=True, verbose_name="Slug",
                            validators=Validators.slug_validators)
    category_photo = models.ImageField(upload_to="category_photo/", null=True, blank=True,
                                       verbose_name="Заглавное фото категории")

    objects = models.Manager()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse_lazy('destination', kwargs={"category_slug": self.slug})

    @classmethod
    def get_categories_with_counts(cls):
        return Category.objects.filter(excursion__is_published=True).annotate(excursion_count=Count('excursion'))

    class Meta:
        verbose_name = "Категорию"
        verbose_name_plural = "Категории"


class Location(models.Model):
    title = models.CharField(max_length=70, verbose_name="Название локации")
    short_info = models.TextField(blank=True, null=True, verbose_name="Короткое описание локации")
    location_photo = models.ImageField(upload_to="location_photo/", null=True, blank=True, verbose_name="Фото локации")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Локация"
        verbose_name_plural = "Локации"
