from typing import Iterable, Optional
from django.db import models
from django.conf import settings
from django.contrib.sessions.models import Session
from django.utils.text import slugify
from django.urls import reverse
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _
import uuid


class Order(models.Model):
    order_id = models.UUIDField(verbose_name=_('order_id'), default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             verbose_name=_('user'),
                             related_name='order_user',
                             on_delete=models.CASCADE)
    cart = models.ForeignKey('cart.Cart',
                             verbose_name=_('cart'),
                             related_name='order_cart')
    items = models.ManyToManyField('cart.CartItem')
    slug = models.SlugField(blank=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_paid = models.BooleanField(verbose_name=_('is paid'), default=False)
    is_completed = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs) -> None:
        self.slug = slugify(self.order_id)
        return super().save(*args, **kwargs)

    @property
    def get_total_price(self):
        total_price = self.items.aggregate(total=models.Sum(models.F('quantity') * models.F('product__price')))['total']
        return total_price or 0

    @property
    def complete_order(self):
        if not self.is_completed:
            with models.Model._meta.db_table_class.objects.select_for_update().filter(pk=self.pk):
                self.refresh_from_db()
                if self.is_completed:
                    return False
                for item in self.items.all():
                    if item.product.reduce_quantity(item.quantity):
                        item.save()
                    else:
                        return False
                self.is_completed = True
                self.save()
                return True
        return False

    def __str__(self):
        return f"Order - {self.user.username}"
