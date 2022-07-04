from dataclasses import field
from django import forms

from .models import Pupil, Teacher, Gallery, Group, Course, Location, ContactMsg, SocialName, Links, SingCourse



class PupilForm(forms.ModelForm):
    class Meta:
        model = Pupil
        exclude = '__all__'
        widgets = {
            'birth': forms.DateInput(attrs={'type': 'date'}),
            'author': forms.HiddenInput
        }

        
class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = '__all__'
        widgets = {
            'author': forms.HiddenInput
        }

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = '__all__'
        widgets = {
            'lesson_time': forms.TimeInput(attrs={'type': 'time'}),
            'author': forms.HiddenInput

        }


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'
        widgets = {
            'author': forms.HiddenInput
        }


class GalleryForm(forms.ModelForm):
    class Meta:
        model = Gallery
        fields = '__all__'
        widgets = {
            'author': forms.HiddenInput
        }
        

class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = '__all__'
        widgets = {
            'author': forms.HiddenInput
        }
        

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMsg
        fields = '__all__'


SocialForm = forms.modelform_factory(SocialName, fields='__all__', widgets = {'author': forms.HiddenInput})
LinksForm = forms.inlineformset_factory(SocialName, Links, fields='__all__', extra=5, can_delete_extra=False)


class SignCourseForm(forms.ModelForm):
    class Meta:
        model = SingCourse
        fields = '__all__'

        widgets = {
        }