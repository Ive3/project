from django.db import models
from taggit.managers import TaggableManager
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.



class Picture(models.Model): 
    class TYPEofIMAGE(models.TextChoices):
        D2 = ('3D', '3D')
        D3 = ('2D', '2D')
        __empty__ = 'Choose image type'
    name = models.CharField(max_length=20)
    description = RichTextUploadingField()
    tags = TaggableManager()
    image = models.ImageField(upload_to='gallery/images/%y/%m/%d/')
    image_type = models.CharField(max_length=2, choices=TYPEofIMAGE.choices)
    views = models.PositiveIntegerField(default=0, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


# Ip for count views -----------------------------------------------------------
class IpModel(models.Model):
    ip = models.CharField(max_length=100, blank=True, null=True)
    picture = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return '%s - %s' % (self.ip, self.picture)