from django.db import models
import datetime
from multiselectfield import MultiSelectField
from django.contrib.auth.models import User
from easy_thumbnails.fields import ThumbnailerImageField
# Create your models here.


class CourseImage(models.Model):
    name = models.CharField(max_length=20)
    icon = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=30)
    image = models.ForeignKey(CourseImage, blank=True, null=True, on_delete=models.PROTECT)
    who_can = models.CharField(max_length=255)
    countinue = models.CharField(max_length=255)
    level = models.CharField(max_length=255)
    price = models.PositiveIntegerField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Location(models.Model):
    image = ThumbnailerImageField(resize_source={'size': (400, 0), 'crop':'scale', 'quantity':90}, upload_to='landingpage/location/')
    street = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    subway = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)


class Gallery(models.Model):
    
    image = models.ImageField(upload_to='landingpage/gallery/')
    description = models.CharField(max_length=150)
    author = models.ForeignKey(User, on_delete=models.CASCADE)




class Teacher(models.Model):
    name = models.CharField(max_length=30)
    image = ThumbnailerImageField(resize_source={'size': (400, 0), 'crop':'scale', 'quantity':90},upload_to='landingpage/teacher/', blank=True, null=True)
    expirience = models.CharField(max_length=255)
    strong_side = models.CharField(max_length=255)
    achievement = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Group(models.Model):
    LEVEL = (
        (None, 'LEVEL'),
        ('A1', 'A1'),
        ('A2', 'A2'),
        ('B1', 'B1'),
        ('B2', 'B2'),
        ('C1', 'C1'),
        ('C2', 'C2'),
    )
    DAYS_OF_WEEK = (
        (None, "Days of week"),
        (1, 'Monday'),
        (2, 'Tuesday'),
        (3, 'Wednesday'),
        (4, 'Thursday'),
        (5, 'Friday'),
        (6, 'Saturday'),
    )
    lesson_time = models.TimeField()
    days_of_week = MultiSelectField(choices=DAYS_OF_WEEK, max_length=10, max_choices=3)
    teacher = models.ForeignKey('Teacher', on_delete=models.PROTECT)
    level = models.CharField(max_length=2, choices=LEVEL)
    creaded_at = models.DateField(auto_now_add=True)
    exists = models.BooleanField(default=0)
    name = models.CharField(max_length=20, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name

        
class Pupil(models.Model):
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    phone = models.PositiveIntegerField(unique=True)
    birth = models.DateField()
    group = models.ForeignKey(Group, on_delete=models.PROTECT)
    paid = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return '%s %s' % (self.name, self.surname)

    def age(self):
        age = datetime.date.today().year - int(self.birth.strftime('%Y'))
        return age




# Social name -----------------------------------------------------------------------
class SocialName(models.Model):
    name = models.CharField(max_length=40)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


# Links for Social name ----------------------------------------------------------------
class Links(models.Model):
    name = models.ForeignKey(SocialName, on_delete=models.CASCADE)
    links = models.URLField(blank=True, null=True)


# Message -------------------------------------------------
class ContactMsg(models.Model):
    name = models.CharField(max_length=50)
    phone = models.PositiveBigIntegerField()
    sent = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s' % (self.name, self.phone)
    
    class Meta:
        ordering = ['-sent']


# sign up to course-------------------------------------------
class SingCourse(models.Model):
    LEVEL = (
        (None, 'LEVEL'),
        ('A1', 'A1'),
        ('A2', 'A2'),
        ('B1', 'B1'),
        ('B2', 'B2'),
        ('C1', 'C1'),
        ('C2', 'C2'),
    )
    name = models.CharField(max_length=50)
    phone = models.PositiveBigIntegerField(help_text='123456789')
    sent = models.DateTimeField(auto_now_add=True)
    level = models.CharField(max_length=2, choices=LEVEL)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return '%s - %s' % (self.name, self.phone)