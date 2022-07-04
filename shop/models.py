import datetime
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django_resized import ResizedImageField
from easy_thumbnails.fields import ThumbnailerImageField
from ckeditor_uploader.fields import RichTextUploadingField
# Create your models here.


# Category -------------------------------------------------------------
class SuperCategory(models.Model):
    name = models.CharField(max_length=10)
    image = ResizedImageField(size=[320, 240], crop=['middle', 'center'], upload_to='shop/supcategory')


    def __str__(self):
        return self.name


class SubCategory(models.Model):
    sup_category = models.ForeignKey(SuperCategory, on_delete=models.PROTECT)
    name = models.CharField(max_length=10)
    image = ResizedImageField(size=[320, 240], crop=['middle', 'center'], upload_to='shop/subcategory')
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return '{0} - {1}'.format(self.sup_category, self.name)
    
    class Meta:
        ordering = ['sup_category', 'name']


# Product -------------------------------------------------------------
class Product(models.Model):
    name = models.CharField(max_length=20, db_index=True)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(SubCategory, on_delete=models.PROTECT)
    description = RichTextUploadingField()
    info = RichTextUploadingField(config_name='simple')
    thumbnail = ThumbnailerImageField(resize_source={'size': (300, 0), 'crop':'scale'}, upload_to='shop/product/thumbnail/%Y/%d/%m/')
    created_at = models.DateTimeField(auto_now_add=True)
    changed_at = models.DateTimeField(auto_now=True)
    price = models.PositiveIntegerField(default=0)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    views = models.PositiveIntegerField(default=0)

    def get_absolute_url(self):
        return reverse('shop:product_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        for ei in self.extraimage_set.all():
            ei.delete()
        super().delete(*args, **kwargs)

    class Meta:
        ordering = ['-created_at', 'name']


# Extra images for product ------------------------------------------------------------
class ExtraImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = ThumbnailerImageField(resize_source={'size': (700, 0), 'crop':'scale', 'quantity':90}, upload_to='shop/image/%Y/%d/%m/')


# Ip for count views -----------------------------------------------------------
class IpModel(models.Model):
    ip = models.CharField(max_length=100, blank=True, null=True)
    product = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return '%s - %s' % (self.ip, self.product)


# Ip for count views -----------------------------------------------------------
class IpCategory(models.Model):
    ip = models.CharField(max_length=100, blank=True, null=True)
    sub_categories = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return '%s - %s' % (self.ip, self.sub_categories)


# Order --------------------------------------------------------
class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.PositiveIntegerField()
    address = models.CharField(max_length=255, default='', blank=True)
    phone = models.CharField(max_length=30, default='', blank=True)
    date = models.DateTimeField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)

    def __str__(self):
        return '%s - %s' % (self.customer, self.product)

    def place_order(self):
        self.save()

    @staticmethod
    def customer_orders(customer_id):
        return Order.objects.filter(customer=customer_id).order_by('-date')




# About -----------------------------------------------------
class About(models.Model):
    name = models.CharField(max_length=20)
    phone = models.CharField(max_length=20, unique=True)
    address1 = models.CharField(max_length=100)
    address2 = models.CharField(max_length=100)
    description = RichTextUploadingField()
    banner = ThumbnailerImageField(resize_source={'size': (1000, 0), 'crop': 'scale', 'quality': 80}, upload_to='shop/about/banner/')
    show = models.BooleanField(default=False)
    
    def delete(self, *args, **kwargs):
        for c in self.carousel_set.all():
            c.delete()
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.name

# Carousel -----------------------------------------------------------------
class Carousel(models.Model):
    name = models.ForeignKey(About, on_delete=models.CASCADE)
    image = ThumbnailerImageField(resize_source={'size': (1000, 0), 'crop': 'scale', 'quality': 80}, upload_to='shop/about/carousel/')

