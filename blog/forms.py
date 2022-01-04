from django import forms
from django.forms import widgets
from django.forms.widgets import ClearableFileInput, TextInput,Textarea,RadioSelect
from . import models


class TicketForm(forms.ModelForm):
    class Meta:
        model = models.Ticket
        fields = ["title","description","image"]
        widgets = {
            'title': TextInput(attrs={
                                "placeholder":"Titre du livre",
                                "class":"form-title"
                                }),
            'description': Textarea(attrs={
                                "placeholder":"Description du ticket",
                                "class":"form-desc"}),
            'image': ClearableFileInput(attrs={
                "id":"img_file",
            })
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = models.Review
        fields = ["headline","rating","body"]
        widgets ={
            'headline': TextInput(attrs={
                                "placeholder":"Titre",
                                "class":"form-title"
                                }),
            'body': Textarea(attrs={
                                "placeholder":"Commentaire",
                                "class":"form-desc",
                                }),
            'rating': RadioSelect(attrs={
                "class":"rating",
            },choices=[("1",1),("2",2),("3",3),("4",4),("5",5)]),
            }
        labels = {"headline":"Titre","body":"Commentaire","rating":"Note"}

class FollowForm(forms.Form):
    username = forms.CharField(label="",widget=TextInput({"placeholder":"Nom d'utilisateur","class":"form-title"}))