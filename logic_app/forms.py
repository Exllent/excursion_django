from django import forms
from django.core.validators import RegexValidator, MinLengthValidator, MaxLengthValidator
from pytz import timezone
from datetime import datetime, timedelta


def current_date_msk():
    current_datetime_utc = datetime.utcnow()
    current_datetime_msk = timezone('Europe/Moscow').localize(current_datetime_utc)
    return current_datetime_msk.date()


class Application(forms.Form):
    name = forms.CharField(
        label='Ваше имя',
        validators=[
            MinLengthValidator(2, message='Имя слишком короткое'),
            MaxLengthValidator(50, message='Имя слишком длинное'),
        ],
        widget=forms.TextInput(
            attrs={
                'class': 'form-control p-4',
            }
        )
    )
    date_excursion = forms.CharField(
        label="Дата экскурсии",
        widget=forms.DateInput(
            attrs={
                'class': 'form-control p-4 datetimepicker-input',
                'type': 'date',
                'min': current_date_msk(),
                'max': current_date_msk() + timedelta(days=365),
            }
        )
    )
    number_phone = forms.CharField(
        label='Номер телефона',
        validators=[
            RegexValidator(
                regex=r'^\+?\d{8,15}$',
                message='неправильный номер'
            )
        ],
        widget=forms.TextInput(
            attrs={
                'type': 'tel',
                'id': 'phone',
                'class': 'form-control p-4',
                'name': 'phone',
            }
        )
    )
    people = forms.IntegerField(
        label="Сколько вас будет",
        widget=forms.NumberInput(
            attrs={
                'type': 'range',
                'min': '1',
                'max': '11',
                'step': '1',
                'id': 'customRange3',
                'style': 'color: rgb(122, 183, 48);'
            }
        )
    )
    comments = forms.CharField(
        label='Оставить пожелание',
        required=False,
        widget=forms.Textarea(
            attrs={
                'rows': 3,
                'style': 'resize:none;',
                'class': 'form-control p-4',
            }
        )
    )
