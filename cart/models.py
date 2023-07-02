from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.utils.text import slugify
from django.urls import reverse
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             verbose_name=_('user'),
                             on_delete=models.CASCADE,
                             related_name='cart_user',
                             null=True,
                             blank=True)
    session = models.ForeignKey(Session,
                                verbose_name=_('session'),
                                on_delete=models.CASCADE,
                                related_name='cart_session',
                                null=True,
                                blank=True)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Cart'
        verbose_name_plural = 'Cart'

    def __str__(self):
        return f"Cart - {self.user.username if self.user else self.session.session_key}"

    @property
    def total_price(self):
        total_price = self.cart_items.aggregate(total=models.Sum(models.F('quantity') * models.F('product__price')))['total']
        return total_price or 0

    def add_to_cart(self, product, quantity=1):
        if self.user:
            cart_item, created = self.cart_items.get_or_create(product=product)
            cart_item.quantity += quantity
            cart_item.save()
        else:
            cart_item, created = self.cart_items.get_or_create(product=product, session=self.session)
            if not created:
                cart_item.quantity += quantity
                cart_item.save()

    def remove_from_cart(self, product):
        if self.user:
            self.cart_items.filter(product=product).delete()
        else:
            self.cart_items.filter(product=product, session=self.session).delete()

    def clear_cart(self):
        if self.user:
            self.cart_items.all().delete()
        else:
            self.cart_items.filter(session=self.session).delete()


class CartItem(models.Model):
    cart = models.ForeignKey('Cart',
                             verbose_name=_('cart'),
                             on_delete=models.CASCADE,
                             related_name='cart_item_cart')
    product = models.ForeignKey('product.Product',
                                verbose_name=_('product'),
                                related_name='cart_item_product',
                                on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1,
                                           verbose_name=_('quantity'),
                                           validators=[MinValueValidator(1)])
    # session = models.ForeignKey(Session,on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = 'CartItem'
        verbose_name_plural = 'CartItem'
    
    @property
    def price(self):
        return (self.product.price - self.product.discount) * self.quantity

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"
