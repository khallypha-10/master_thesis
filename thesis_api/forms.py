from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from . models import Prescriptions




class PatientSignupForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    class Meta:
        model = User 
        fields = ['username', 'email', 'password1', 'password2']


    def __init__(self, *args, **kwargs):
        super(PatientSignupForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class']= 'form-control'
        self.fields['email'].widget.attrs['class']= 'form-control'
        self.fields['password1'].widget.attrs['class']= 'form-control'
        self.fields['password2'].widget.attrs['class']= 'form-control'
        

class DoctorSignupForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    class Meta:
        model = User 
        fields = ['username', 'email', 'password1', 'password2']


    def __init__(self, *args, **kwargs):
        super(DoctorSignupForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class']= 'form-control'
        self.fields['email'].widget.attrs['class']= 'form-control'
        self.fields['password1'].widget.attrs['class']= 'form-control'
        self.fields['password2'].widget.attrs['class']= 'form-control'



class PrescriptionForm(ModelForm):
    class Meta:
        model = Prescriptions 
        exclude = ['prescribed_by', 'slug', 'prescribed_on']

    def __init__(self, *args, **kwargs):
        super(PrescriptionForm, self).__init__(*args, **kwargs)

        self.fields['prescribe_for'].widget.attrs['class']= 'form-control'
        self.fields['medication'].widget.attrs['class']= 'form-control'