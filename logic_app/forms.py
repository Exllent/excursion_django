from django import forms
from django.core.validators import RegexValidator, MinLengthValidator, MaxLengthValidator
from .utils import current_date_msk_with_timedelta, current_date_msk


class BookingForm(forms.Form):
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
                'max': current_date_msk_with_timedelta(days=365),
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
    wishes = forms.CharField(
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
