from django.db import models, migrations
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django_resized import ResizedImageField
from easy_thumbnails.fields import ThumbnailerImageField
from ckeditor_uploader.fields import RichTextUploadingField
# Create your models here.



# Validate image in extra images -----------------------------------------------------------
def validate_image(fieldfile_obj):
    filesize = fieldfile_obj.file.size
    megabyte_limit = 2.0
    if filesize > megabyte_limit*1024*1024:
        raise ValidationError("Max image size is %sMB" % str(megabyte_limit))


# Validate vidoe in post -----------------------------------------------------------
def validate_video(video_obj):
    videisize = video_obj.file.size
    megabyte_limit = 50.0
    if videisize > megabyte_limit * 1024 * 1024:
        raise ValidationError('Max video size is %sMB' % str(megabyte_limit))


# Ip for count views -----------------------------------------------------------
class IpModel(models.Model):
    ip = models.CharField(max_length=100, blank=True, null=True)
    post = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return '%s - %s' % (self.ip, self.post)


# Category ------------------------------------------------------------------------
class Category(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='blog/category/image/')
    slug = models.SlugField(max_length=50, unique=True, help_text='Slug must be the same as Name! Use only "-" insted space" " and the others')

    def __str__(self):
        return self.name


# Post ----------------------------------------------------------------------------
class Post(models.Model):
    title = models.CharField(max_length=50, db_index=True)
    slug = models.SlugField(max_length=50, unique=True, help_text='Slug must be the same as Name! Use only "-" insted space" " and the others')
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    short_description = RichTextUploadingField(config_name='base')
    text = RichTextUploadingField()
    video = models.FileField(upload_to='blog/post/vidoe/%Y/%m/%d/', null=True, blank=True, validators=[validate_video], help_text='Max video size is 50 MB!')
    thumbnail = ThumbnailerImageField(resize_source={'size': (800, 0), 'crop': 'scale', 'quality': 80}, upload_to='blog/thumbnail/%Y/%m/%d/')
    created = models.DateTimeField(auto_now_add=True)
    changed = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    show = models.BooleanField(default=True, db_index=True)
    likes = models.ManyToManyField(User, related_name='blog_post', blank=True, null=True, default=0)
    views = models.PositiveIntegerField(default=0, blank=True, null=True)

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.title

    # Remove extra images when delete post ------------------------------------
    def delete(self, *args, **kwargs):
        for ei in self.extraimage_set.all():
            ei.delete()
        super().delete(*args, **kwargs)
    
    class Meta:
        ordering = ['-created']

# extra images for post-----------------------------------------------------------------
class ExtraImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image = ThumbnailerImageField(resize_source={'size': (800, 0), 'crop': 'scale', 'quality': 80},upload_to='blog/post/image/%Y/%m/%d/', blank=True, null=True, validators=[validate_image], help_text='Maximum image size allowed is 2Mb')


# Social name -----------------------------------------------------------------------
class SocialName(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self) -> str:
        return self.name


# Links for Social name ----------------------------------------------------------------
class Links(models.Model):
    name = models.ForeignKey(SocialName, on_delete=models.CASCADE)
    links = models.URLField(blank=True, null=True)


# Comment for post ------------------------------------------------------------------------
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, default='anonim')
    text = RichTextUploadingField(config_name='simple')
    created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return '%s - %s' % (self.name, self.post)

    class Meta:
        ordering = ['-created']


# About --------------------------------------------------------------
class About(models.Model):
    description = RichTextUploadingField()
    image = models.ImageField(upload_to='blog/about/image/', validators=[validate_image], help_text='Maximum image size allowed is 2Mb')
    video = models.FileField(upload_to='blog/about/video/', validators=[validate_video], help_text='Maximum video size is 50 MB!')
    active = models.BooleanField(default=False)