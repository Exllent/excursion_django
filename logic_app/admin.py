from django.contrib import admin, messages
from django.utils.safestring import mark_safe

from .models import Excursion, Category, Location


@admin.register(Excursion)
class ExcursionAdmin(admin.ModelAdmin):
    fields = (
        "title", "slug", "description", "price", "discount", "header_photo", "show_image", "is_published", "category",
        "location")
    readonly_fields = ("slug", "show_image")
    list_display = ("show_image", "title", "slug", "price", "discount", "is_published", "category")
    list_display_links = ("title", "show_image")
    list_editable = ("is_published", "discount", "price", "category")
    list_per_page = 5
    actions = ("set_published", "set_draft")
    search_fields = ("title",)
    list_filter = ("is_published",)
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
    fields = ("title", "short_info", "show_image", "location_photo")
    list_display = ("show_image", "title")
    readonly_fields = ("show_image",)
    list_display_links = ("title", "show_image")
    search_fields = ("title",)
    list_filter = ("title",)
    save_on_top = True

    @admin.display(description="Фото локации")
    def show_image(self, location: Location):
        photo = location.location_photo
        if photo:
            return mark_safe(f"<img src={photo.url} width=100>")
        else:
            return "Без фото"
