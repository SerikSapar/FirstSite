from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.forms import ModelForm, Textarea, DateTimeInput, CheckboxSelectMultiple

from .models import *


class ShiForm(ModelForm):
    class Meta:
        model = Shi
        fields = ['title', 'description', 'logo', 'time', 'short_description']

        widgets = {
            'title': Textarea(attrs={
                'class': 'Add1',
                'placeholder': 'Название',
            }),
            'short_description': Textarea(attrs={
                'class': 'Add21',
                'placeholder': 'Краткое описание',
            }),
            'description': Textarea(attrs={
                'class': 'Add2',
                'placeholder': 'Описание',
            }),
            'time': DateTimeInput(attrs={
                'class': 'transform',
                'placeholder': 'Дата и Время',
                'type': 'date'
            }),

        }


class CourseForm(ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'logo', 'rubric', 'lessons']

        widgets = {
            'title': Textarea(attrs={
                'class': 'Add1',
                'placeholder': 'Название',
            }),
            'short_description': Textarea(attrs={
                'class': 'Add21',
                'placeholder': 'Краткое описание',
            }),
            'description': Textarea(attrs={
                'class': 'Add2',
                'placeholder': 'Описание',
            }),
            'time': DateTimeInput(attrs={
                'class': 'transform',
                'placeholder': 'Дата и Время',
            }),
        }

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'email')

class ProfileUser(ModelForm):
    class Meta:
        model = User
        fields = '__all__'


class UserProf(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'short_description', 'photo']
        widgets = {
            'short_description': Textarea(attrs={
                'class': 'Add31',
            })}

