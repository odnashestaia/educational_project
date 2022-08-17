from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.db import models
from django.urls import reverse
from django.utils.crypto import get_random_string


def get_name_file(instance, filename):
    return '/'.join([get_random_string(length=5) + '_' + filename])


class User(AbstractUser):
    name = models.CharField(max_length=254, verbose_name='Имя', blank=False)
    surname = models.CharField(max_length=254, verbose_name='Фамилия', blank=False)
    patronymic = models.CharField(max_length=254, verbose_name='Отчество', blank=True)
    username = models.CharField(max_length=254, verbose_name='Логин', unique=True, blank=False)
    emain = models.CharField(max_length=254, verbose_name='Почта', unique=True, blank=False)
    password = models.CharField(max_length=254, verbose_name='Пароль', blank=False)
    role = models.CharField(max_length=254, verbose_name='Роль',
                            choices=(('admin', 'Администратор'), ('user', 'Пользователь')), default='user')

    def full_name(self):
        return ' '.join([self.name, self.surname, self.patronymic])

    def __str__(self):
        return self.full_name()


class Product(models.Model):
    name = models.CharField(max_length=254, verbose_name='Имя', blank=False)
    photo_file = models.ImageField(max_length=254, upload_to=get_name_file, blank=True, null=True,
                                   validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg'])])
    price = models.DecimalField(verbose_name='Стоимость', max_digits=10, decimal_places=2, blank=False, default=0.00)
    category = models.ForeignKey('Category', verbose_name='Категория', on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('product', args=[str(self.id)])

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=254, verbose_name="Наименование", blank=False)

    def __str__(self):
        return self.name


class Orders(models.Model):
    STATUS_CHOUSE = [
        ('new', 'Новые'),
        ('exsept', 'Принятые'),
        ('cancelled', 'Отменные')
    ]
    date = models.DateTimeField(verbose_name='Дата добавления', auto_now_add=True)
    role = models.CharField(max_length=254, verbose_name='Статус',
                            choices=STATUS_CHOUSE,
                            default='new')
    user = models.ForeignKey('User', verbose_name='Пользователь', on_delete=models.CASCADE)
    reason = models.CharField(max_length=1000, verbose_name='Причина отказа', blank=False)
    products = models.ManyToManyField(Product, through='Goods', related_name='orders')

    def status_verbose(self):
        return dict(self.STATUS_CHOUSE)[self.role]

    def count_product(self):
        count_product = 0
        for item in self.goods_set.all():
            count_product += item.count
        return count_product

    def __str__(self):
        return str(self.date.ctime()) + '|' + str(self.user.full_name()) + '| Количество ' + str(self.count_product())


class Goods(models.Model):
    orders = models.ForeignKey(Orders, verbose_name='Заказы', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name='Товар', on_delete=models.CASCADE)
    price = models.DecimalField(verbose_name='Стоимость', max_digits=10, decimal_places=2, blank=False, default=0.00)


class Basket(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name='Товар', on_delete=models.CASCADE)
    count = models.IntegerField(verbose_name='Количество', blank=False, default=0)

    def __str__(self):
        return self.product.name + ' - ' + str(self.count)
