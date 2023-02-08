from dataclasses import field, fields
from operator import mod
from pyexpat import model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from stack.models import Questions

class RegistrationForm(UserCreationForm):

    class Meta:
        model=User
        fields=[
            "first_name",
            "last_name",
            "username",
            "email",
            "password1",
            "password2",
        ]

class LoginForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField()

class QuestionForm(forms.ModelForm):
    class Meta:
        model=Questions
        fields=[
            "question",
            "image",
        ]
        

        widgets={
            "question":forms.Textarea(attrs={"class":"form-control","rows":3}),
            "image":forms.FileInput(attrs={"class":"form-select"})
                }


  