from django import forms
from django.core.validators import RegexValidator, MinValueValidator
from pytz import timezone
from datetime import datetime, timedelta


def current_date_msk():
    current_datetime_utc = datetime.utcnow()
    current_datetime_msk = timezone('Europe/Moscow').localize(current_datetime_utc)
    return current_datetime_msk.date()


class Application(forms.Form):
    CHOICES = [
        (0, 'Сколько человек'),
        (1, 'Один'),
        (2, 'Двое'),
        (3, 'Трое'),
        (4, 'Четверо'),
        (5, 'Пятеро'),
        (6, 'Больше'),
    ]
    quantity_person = forms.ChoiceField(choices=CHOICES, widget=forms.Select(
        attrs={'class': 'custom-select px-4', 'style': 'height: 47px;'}),
                                        )
    date_excursion = forms.CharField(widget=forms.DateInput(
        attrs={'class': 'form-control p-4 datetimepicker-input', 'type': 'date',
               'min': current_date_msk(),
               'max': current_date_msk() + timedelta(days=365),
               }))

    number_phone = forms.CharField(
        validators=[RegexValidator(regex=r'^\+?\d{9,15}$', message='Введите корректный номер телефона.')],
        widget=forms.TextInput(
            attrs={'type': 'tel', 'id': 'phone', 'class': 'form-control p-4',
                   'name': 'phone',
                   'placeholder': 'Номер телефона'}))
