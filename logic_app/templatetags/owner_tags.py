from django import template

register = template.Library()


@register.inclusion_tag("logic_app/includes/des.html")
def show_destination(categories: list):
    return {"categories": categories}


@register.inclusion_tag("logic_app/includes/pack.html")
def show_package(excursion: list):
    return {"excursion": excursion}
