from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import Product, ExtraImage, SubCategory


class CartAddForm(forms.Form):
    quantity = forms.IntegerField(widget=forms.NumberInput(
        attrs={'class': 'form-control'}), label='Qnt:', min_value=0)
    update = forms.BooleanField(
        required=False, initial=False, widget=forms.HiddenInput)


# Add Product form ----------------------------------------------------------------
class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ('views',)
        widgets = {
            'author': forms.HiddenInput,
            'desctiption': CKEditorUploadingWidget(),
            'info': CKEditorUploadingWidget(),
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'slug': forms.TextInput(attrs={'class':'form-control'}),
            'category': forms.Select(attrs={'class':'form-control'}),
            'thumbnail': forms.FileInput(attrs={'class':'form-control'}),
            'price': forms.NumberInput(attrs={'class':'form-control'}),
        }


# Extra images form for product form --------------------------------------------------
ExtraImageForm = forms.inlineformset_factory(Product, ExtraImage, fields='__all__', extra=5, can_delete_extra=False, widgets={
    'image': forms.FileInput(attrs={'class': 'form-control'})
    })
