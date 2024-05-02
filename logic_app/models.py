from django.db import models
from django.core.validators import MaxLengthValidator, MinLengthValidator, MaxValueValidator, MinValueValidator
from django.db.models import OuterRef, Count, Subquery
from django.urls import reverse_lazy
from pytils.translit import slugify


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=True)


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
    price = models.IntegerField(verbose_name="Цена", validators=Validators.price_validators)
    discount = models.IntegerField(default=0, verbose_name="Скидка (%)",
                                   validators=Validators.discount_validators, choices=choices_discount)
    header_photo = models.ImageField(upload_to="header_photo/", blank=True, null=True,
                                     verbose_name="Заглавное фото экскурсии")
    description = models.TextField(blank=True, null=True, verbose_name="Описание экскурсии")
    is_published = models.BooleanField(choices=status_published,
                                       default=False,
                                       verbose_name="Статус")
    top = models.BooleanField(choices=excursion_top, default=False, verbose_name="Отображение экскурсии вверху")
    category = models.ForeignKey("Category", blank=True, null=True, on_delete=models.SET_NULL, related_name='excursion',
                                 verbose_name="Категории")
    location = models.ManyToManyField("Location", blank=True, related_name='excursion', verbose_name="Локации")

    objects = models.Manager()
    published = PublishedManager()

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
    def categories_with_excursion_data(cls):
        subquery = Excursion.objects.filter(
            category_id=OuterRef('pk'), is_published=True, top=True
        ).values('title', 'description', 'price', 'slug', 'discount', 'header_photo')[:1]
        categories_with_excursion_data = cls.objects.annotate(
            excursion_count=Count('excursion'),
            excursion_title=Subquery(subquery.values('title'), output_field=models.CharField()),
            excursion_description=Subquery(subquery.values('description'), output_field=models.TextField()),
            excursion_price=Subquery(subquery.values('price'), output_field=models.IntegerField()),
            excursion_slug=Subquery(subquery.values('slug'), output_field=models.SlugField()),
            excursion_discount=Subquery(subquery.values('discount'), output_field=models.IntegerField()),
            excursion_header_photo=Subquery(subquery.values('header_photo'), output_field=models.URLField())
        )
        return categories_with_excursion_data

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
