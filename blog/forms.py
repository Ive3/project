from django import forms
from captcha.fields import CaptchaField
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import Post, ExtraImage, Category, Comment


# Create Post form ------------------------------------------------------------------------
class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ('likes', 'views')
        widgets = {
            'author': forms.HiddenInput,
            'text': CKEditorUploadingWidget(),
            'short_description': CKEditorUploadingWidget(),
        }


# extra images for Post form ------------------------------------------------------------------------
ExtraImageForm = forms.inlineformset_factory(Post, ExtraImage, fields='__all__', extra=5, can_delete_extra=False)


# Search form ------------------------------------------------------------------------
class SearchForm(forms.Form):
    keyword = forms.CharField(max_length=50)


# Create category form ------------------------------------------------------------------------
CreateCategoryForm = forms.modelformset_factory(Category, fields='__all__', can_delete=False, extra=5)


# user comment form -------------------------------------------------------------------
class UserCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ('is_active',)
        widgets = {
            'post': forms.HiddenInput,
            'text': CKEditorUploadingWidget(),
        }


# guest comment form -------------------------------------------------------------------
class GuestCommentForm(forms.ModelForm):
    captcha = CaptchaField()

    class Meta:
        model = Comment
        exclude = ('is_active',)
        widgets = {
            'post': forms.HiddenInput,
            'text': CKEditorUploadingWidget(),

        }