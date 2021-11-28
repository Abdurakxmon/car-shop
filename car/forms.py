from django import forms
from .models import Comment, Contact,Product, Profile

#######
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
#######

class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = '__all__'
		exclude = ('post','parent')
		widgets = {
			'message':forms.Textarea(attrs={'rows':10,'cols':70}),
		}

class ContactForm(forms.ModelForm):
	class Meta:
		model = Contact
		fields = '__all__'
		widgets = {
			'message':forms.Textarea(attrs={'cols':100,'rows':100}),
		}



class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']


class ProfileForm(forms.ModelForm):
	class Meta:
	    model = Profile
	    fields = '__all__'
	    exclude = ['user']