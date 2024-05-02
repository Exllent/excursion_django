from django import template

register = template.Library()


@register.inclusion_tag("logic_app/includes/des.html")
def show_destination(categories: list):
    print(categories)
    return {"categories": categories}
