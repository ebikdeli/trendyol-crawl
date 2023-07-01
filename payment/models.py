from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
import uuid


class Payment(models.Model):
    payment_id = models.UUIDField(verbose_name=_('payment id'), default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             verbose_name=_('user'),
                             related_name='payment_user',
                             on_delete=models.CASCADE)
    order = models.ForeignKey('order.Order',
                              verbose_name=_('order'),
                              related_name='payment_order',
                              on_delete=models.CASCADE)
    price = models.DecimalField(verbose_name=_('price'), max_digits=10, decimal_places=0)
    is_paid = models.BooleanField(verbose_name=_('is paid'), default=False)
    # Payment choices will be put here
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Payment'
        verbose_name_plural = 'Payment'
    
    def __str__(self) -> str:
        return f'{self.user.user}: {self.payment_id}'
