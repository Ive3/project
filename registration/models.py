from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
# Create your models here.
import datetime

class RegistrationUser(models.Model):
    GENDER = (
        (None, 'choose your gender'),
        ('M', 'Male'),
        ('F', 'Female'),
        ('S', 'Other')
    )
    info = RichTextUploadingField(null=True, config_name='base')
    birth = models.DateField(null=True)
    gender = models.CharField(max_length=1, choices=GENDER)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    def age(self):
        age = datetime.date.today().year - int(self.birth.strftime('%Y'))
        return age