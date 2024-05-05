from django import template

register = template.Library()


@register.inclusion_tag("logic_app/includes/des.html")
def show_destination(categories: list):
    return {"categories": categories}


@register.inclusion_tag("logic_app/includes/pack.html")
def show_package(excursion: list):
    return {"excursion": excursion}


@register.simple_tag()
def digit_to_text(digit: int):
    numbers_dict = {
        1: "одну",
        2: "две",
        3: "три",
        4: "четыре",
        5: "пять",
        6: "шесть",
        7: "семь",
        8: "восемь",
        9: "девять",
        10: "десять",
        11: "одиннадцать",
        12: "двенадцать",
        13: "тринадцать",
        14: "четырнадцать",
        15: "пятнадцать",
        16: "шестнадцать",
        17: "семнадцать",
        18: "восемнадцать",
        19: "девятнадцать",
        20: "двадцать",
        21: "двадцать одну",
        22: "двадцать две",
        23: "двадцать три",
        24: "двадцать четыре",
        25: "двадцать пять",
        26: "двадцать шесть",
        27: "двадцать семь",
        28: "двадцать восемь",
        29: "двадцать девять",
        30: "тридцать"
    }
    return numbers_dict[digit]
