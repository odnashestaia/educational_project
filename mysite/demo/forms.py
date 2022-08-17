from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

from demo.models import User


def validate_password_len(password):
    if len(password) < 6:
        raise ValidationError('Длина пароля не может быть не мение 6 символов')


class RegisterUserForm(forms.ModelForm):
    username = forms.CharField(label='Логин',
                               validators=[RegexValidator('^[a-zA-z0-9-]+$',
                                                          message='Разрешены только латиница, цыфры и тире')],
                               error_messages={
                                   'required': 'Обязательное поле',
                                   'unique': 'Данный логин занят'
                               })
    email = forms.EmailField(label='Адрес Эл. почты',
                             error_messages={
                                 'required': 'Неправильная формат адреса',
                                 'unique': 'Данный адрес занят'
                             })
    password = forms.CharField(label='Пароль',
                               widget=forms.PasswordInput,
                               validators=[validate_password_len],
                               error_messages={
                                   'required': 'Обязательное поле',
                               })
    password2 = forms.CharField(label='Пароль повторно',
                                widget=forms.PasswordInput,
                                error_messages={
                                    'required': 'Обязательное поле',
                                })
    rules = forms.BooleanField(required=True,
                               label='Согласие',
                               error_messages={
                                   'required': 'Обязательное поле',
                               })
    name = forms.CharField(label='Имя',
                           validators=[RegexValidator('^[а-я-А-Я-]+$',
                                                      message='Разрешены только кирилица, цыфры и тире')],
                           error_messages={
                               'required': 'Обязательное поле',
                           })

    surname = forms.CharField(label='Фамилия',
                              validators=[RegexValidator('^[а-я-А-Я-]+$',
                                                         message='Разрешены только кирилица, цыфры и тире')],
                              error_messages={
                                  'required': 'Обязательное поле',
                              })

    def clean(self):
        super.clean()
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password and password2 and password2 != password:
            raise ValidationError({
                'password2': ValidationError('Пароли не совподают', code='password')
            })

    def save(self, commit=True):
        user = super.save(commit=False)
        user.set_password(self.cleaned_data('password'))
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password',
                  'name', 'surname', 'rules')


class OrderForm(forms.ModelForm):
    def clean(self):
        role = self.cleaned_data.get('role')
        reason = self.cleaned_data.get('reason')
        if self.instance.role != 'new':
            raise forms.ValidationError({'role': 'Стаус можно сменить только у новых заказов'})
        if role == 'cancelled' and not reason:
            raise forms.ValidationError({'reason': 'При отказе нужно указать причину'})