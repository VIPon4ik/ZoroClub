from django.forms.models import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import User, Announcment

class UploadedFilesForm(ModelForm):
    class Meta:
        model = Announcment
        fields = ['image']

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']

class AnnouncmentForm(ModelForm):
    class Meta:
        model = Announcment
        fields = ['name','breed','old','sex','documents','purpose','city','description','price']

