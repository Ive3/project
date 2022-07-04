from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from .models import Picture


class PictureForm(forms.ModelForm):
    class Meta:
        model = Picture
        fields = '__all__'
        widgets = {
            'views': forms.widgets.HiddenInput,
            'author': forms.widgets.HiddenInput,
            'description': CKEditorUploadingWidget(),
        }