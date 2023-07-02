from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('name'))
    slug = models.SlugField(unique=True, editable=False)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True, related_name='children')

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Category'
        
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('name'))
    slug = models.SlugField(unique=True, editable=False)
    
    class Meta:
        verbose_name = 'Brand'
        verbose_name_plural = 'Brand'
    
    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey('Category',
                                 verbose_name=_('category'),
                                 on_delete=models.CASCADE,
                                 related_name='product_category')
    brand = models.ForeignKey('Brand',
                              verbose_name=_('brand'),
                              on_delete=models.SET_NULL,
                              related_name='product_brand',
                              blank=True,
                              null=True)
    name = models.CharField(verbose_name=_('name'), max_length=200)
    slug = models.SlugField(unique=True, editable=False)
    description = models.TextField(verbose_name=_('description'), blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=0,
                                verbose_name=_('price'),
                                validators=[MinValueValidator(0)])
    discount = models.DecimalField(max_digits=10, decimal_places=0,
                                   verbose_name=_('discount'),
                                   validators=[MinValueValidator(0)])
    image = models.ImageField(upload_to='products/', verbose_name=_('image'))
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True, verbose_name=_('is active'))
    # quantity_available = models.PositiveIntegerField(default=0,
    #                                                  verbose_name=_('quantity available'),
    #                                                  validators=[MinValueValidator(0)])

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Product'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    # def reduce_quantity(self, quantity):
    #     if self.quantity_available >= quantity:
    #         self.quantity_available -= quantity
    #         self.save()
    #         return True
    #     return False
    
    # def increase_quantity(self, quantity):
    #     self.quantity_available += quantity
    #     self.save()
