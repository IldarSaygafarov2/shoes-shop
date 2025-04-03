from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.timezone import now



class ProductSizes(models.TextChoices):
    SIZE_1 = '39', '39'
    SIZE_2 = '40', '40'
    SIZE_3 = '41', '41'
    SIZE_4 = '42', '42'
    SIZE_5 = '43', '43'
    SIZE_6 = '44', '44'


# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=150, verbose_name='Наименование категории')
    slug = models.SlugField(unique=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE,
                               null=True, blank=True,
                               verbose_name='Категория', related_name='subcategories')

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

    def __repr__(self):
        return f'Категория: pk={self.pk}, title={self.title}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


# ------------------------------------------------------------------------------------------
class Product(models.Model):
    title = models.CharField(max_length=150, verbose_name='Наименование товара')
    price = models.IntegerField(default=0, verbose_name='Цена')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    descriptions = models.TextField(default='There will be a description soon', verbose_name='Описание товара')
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 verbose_name='Категория', related_name='products')
    slug = models.SlugField(unique=True, null=True)
    # duration = models.CharField( max_length=250, verbose_name='Продолжительность')
    # date = models.DateTimeField(default=now, verbose_name='Дата')
    quantity = models.IntegerField(default=0, verbose_name='Количество на складе')
    product_size = models.CharField(choices=ProductSizes, default=ProductSizes.SIZE_1, verbose_name='Размер',
                                    max_length=20)

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.slug})

    def get_first_photo(self):
        if self.images:
            try:
                return self.images.first().image.url
            except:
                return 'https://school544spb.ru/wp-content/uploads/2022/11/file.png'
        else:
            return 'https://school544spb.ru/wp-content/uploads/2022/11/file.png'

    def __str__(self):
        return self.title

    def __repr__(self):
        return f'Товар: pk={self.pk}, title={self.title}, price={self.price}'

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


# ------------------------------------------------------------------------------------------
class Gallery(models.Model):
    image = models.ImageField(upload_to='products/', verbose_name='Изображение')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')

    class Meta:
        verbose_name = 'Изображения'
        verbose_name_plural = 'Галерея товаров'


# ------------------------------------------------------------------------------------------
class Review(models.Model):
    text = models.TextField(verbose_name='Текст отзыва')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.author.username

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


# ------------------------------------------------------------------------------------------
class FavouriteProducts(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name='Избранный товар', on_delete=models.CASCADE)

    def __str__(self):
        return self.product.title

    class Meta:
        verbose_name = 'Избранный товар'
        verbose_name_plural = 'Избранные товары'


class Mail(models.Model):
    mail = models.EmailField(unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.mail

    class Meta:
        verbose_name = 'Почта'
        verbose_name_plural = 'Почтовые адреса'


# ------------------------------------------------------------------------------------------
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, blank=True, null=True)
    first_name = models.CharField(max_length=255, verbose_name='Имя пользователя')
    last_name = models.CharField(max_length=255, verbose_name='Фамилия пользователя')

    def __str__(self):
        return self.first_name

    class Meta:
        verbose_name = 'Покупатель'
        verbose_name_plural = 'Покупатели'


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Покупатель')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время заказа')
    is_completed = models.BooleanField(default=False)  # Is order completed?
    shipping = models.BooleanField(default=True, verbose_name='Доставка')

    def __str__(self):
        return str(self.pk) + ' '

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    @property
    def get_cart_total_price(self):
        order_products = self.orderproduct_set.all()
        total_price = sum([product.get_total_price for product in order_products])
        return total_price

    @property
    def get_cart_total_quantity(self):
        order_products = self.orderproduct_set.all()
        total_quantity = sum([product.quantity for product in order_products])
        return total_quantity


class OrderProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Товар в заказе'
        verbose_name_plural = 'Товары в заказах'

    @property
    def get_total_price(self):
        total_price = self.product.price * self.quantity
        return total_price


class ShippingAddresses(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=255)
    city = models.ForeignKey('City', on_delete=models.CASCADE, verbose_name='Города')
    state = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address

    class Meta:
        verbose_name = 'Адрес доставки'
        verbose_name_plural = 'Адреса доставки'


class City(models.Model):
    city_name = models.CharField(max_length=255, verbose_name='Города')

    def __str__(self):
        return self.city_name

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'