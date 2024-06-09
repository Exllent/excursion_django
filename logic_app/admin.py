from django.contrib import admin, messages
from django.utils.safestring import mark_safe

from .models import Excursion, Category, Location, Review, Booking, GalleryReview, Employee


@admin.register(Excursion)
class ExcursionAdmin(admin.ModelAdmin):
    fields = (
        "title", "slug", "duration", "geo", "description", "price", "discount", "header_photo", "show_image",
        "is_published", "top",
        "category",
        "location"
    )
    readonly_fields = ("slug", "show_image")
    list_display = ("show_image", "title", "slug", "duration", "geo", "price", "discount", "is_published", "top")
    list_display_links = ("title", "show_image")
    list_editable = ("is_published", "top", "discount", "price")
    list_per_page = 5
    actions = ("set_published", "set_draft")
    search_fields = ("title",)
    list_filter = ("is_published", "top")
    save_on_top = True

    @admin.display(description="Фото экскурсии")
    def show_image(self, excursion: Excursion):
        photo = excursion.header_photo
        if photo:
            return mark_safe(f"<img src={photo.url} width=100>")
        else:
            return "Без фото"

    @admin.action(description="Опубликовать экскурсии")
    def set_published(self, request, queryset):
        count = queryset.update(is_published=True)
        if count != 1:
            self.message_user(request=request, message=f"Опубликовано {count} экскурсий")
        else:
            self.message_user(request=request, message=f"Опубликована одна экскурсия")

    @admin.action(description="Добавить экскурсии в черновик")
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=False)
        if count != 1:
            self.message_user(request, f"Добавлено в черновик {count} экскурсий", messages.WARNING)
        else:
            self.message_user(request, f"Одна экскурсия добавлена в черновик ", messages.WARNING)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fields = ("title", "slug", "show_image", "category_photo")
    list_display = ("show_image", "title", "slug")
    readonly_fields = ("slug", "show_image")
    list_display_links = ("title", "show_image")
    search_fields = ("title",)
    list_filter = ("title",)
    save_on_top = True

    @admin.display(description="Фото категории")
    def show_image(self, category: Category):
        photo = category.category_photo
        if photo:
            return mark_safe(f"<img src={photo.url} width=100>")
        else:
            return "Без фото"


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    fields = ("title", "short_info", "group_id", "show_image", "location_photo")
    list_display = ("show_image", "title")
    readonly_fields = ("show_image",)
    list_display_links = ("title", "show_image")
    search_fields = ("title",)
    list_filter = ("title",)
    list_per_page = 6
    save_on_top = True

    @admin.display(description="Фото локации")
    def show_image(self, location: Location):
        photo = location.location_photo
        if photo:
            return mark_safe(f"<img src={photo.url} width=100>")
        else:
            return "Без фото"


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    fields = (
        "name", "phone_number", "number_of_people",
        "created_at", "user_agent", "wishes",
        "excursion",
    )
    readonly_fields = fields
    list_display = (
        "name", "phone_number", "number_of_people",
        "created_at", "excursion",
    )
    list_display_links = ("name", "phone_number")
    list_per_page = 10
    search_fields = ("name", "created_at")
    list_filter = ("name", "created_at", "excursion")
    save_on_top = True


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    fields = ("name", "review", "created_at", "excursion")
    list_display = ("name", "review", "created_at", "excursion")
    list_display_links = ("name",)
    list_editable = ("review", "created_at", "excursion")
    list_filter = ("created_at", "excursion")
    list_per_page = 5
    save_on_top = True


@admin.register(GalleryReview)
class GalleryReviewAdmin(admin.ModelAdmin):
    fields = ("review_photo",)
    list_display = ("id", "show_image")
    readonly_fields = ("show_image",)
    list_display_links = ("id", "show_image")
    list_per_page = 10

    @admin.display(description="Скриншот отзыва")
    def show_image(self, gallery_review: GalleryReview):
        return mark_safe(f"<img src={gallery_review.review_photo.url} width=100>")


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    fields = ("name", "position", "employee_photo")
    list_display = ("id", "name", "position", "employee_photo", "show_image")
    list_display_links = ("id", "show_image")
    list_filter = ("id",)
    list_per_page = 5
    save_on_top = True

    @admin.display(description="Фото агента")
    def show_image(self, employee: Employee):
        return mark_safe(f"<img src={employee.employee_photo.url} width=100>")
