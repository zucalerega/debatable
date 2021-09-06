from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Report
from posts.models import Like

class LikeForm(forms.ModelForm):
    post = forms.IntegerField(widget=forms.HiddenInput(), required=False, initial=0)
    action = forms.CharField(widget=forms.HiddenInput(), required=False, initial='True')

    class Meta:
        model=Like
        fields=['post', 'action']

class UserRegisterForm(UserCreationForm):
    email=forms.EmailField()

    class Meta:
        model=User
        fields=['username', 'email','password1', 'password2']

class UserUpdateForm(forms.ModelForm):

    email=forms.EmailField()

    class Meta:
        model=User
        fields=['email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model=Profile
        fields=['image', 'bio']

class ReportForm(forms.ModelForm):
    # reporter = forms.CharField(widget=forms.HiddenInput(), required=False, initial='reporter')
    # offender = forms.CharField(widget=forms.HiddenInput(), required=False, initial='offe')
    profanity = forms.BooleanField(required=False)
    discrimination = forms.BooleanField(required=False)
    inappropriate = forms.BooleanField(required=False)
    sexual = forms.BooleanField(required=False)
    bot = forms.BooleanField(required=False)
    message = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Bio here"}))
    class Meta:
        model = Report
        fields = ['profanity', 'discrimination', 'inappropriate', 'sexual', 'bot', 'message']

class QuizForm(forms.ModelForm):
    Question_1_ = forms.DecimalField(required=True, max_value=20, min_value=0, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'question'}))
    q2_ = forms.DecimalField(required=True, max_value=20, min_value=0, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'question'}))
    q3_ = forms.DecimalField(required=True, max_value=20, min_value=0, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'question'}))
    q4_ = forms.DecimalField(required=True, max_value=20, min_value=0, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'question'}))
    q5_ = forms.DecimalField(required=True, max_value=20, min_value=0, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'question'}))
    q6 = forms.DecimalField(required=True, max_value=20, min_value=0, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'question'}))
    q7 = forms.DecimalField(required=True, max_value=20, min_value=0, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'question'}))
    q8 = forms.DecimalField(required=True, max_value=20, min_value=0, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'question'}))
    q9 = forms.DecimalField(required=True, max_value=20, min_value=0, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'question'}))
    q10 = forms.DecimalField(required=True, max_value=20, min_value=0, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'question'}))

    class Meta:
        model = Profile
        fields = []
