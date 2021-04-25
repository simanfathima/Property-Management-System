from django import forms
from .models import Sell,Buy,Rent,Tenant,Appointment,Filter
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



class DateInput(forms.DateInput):
    input_type = 'date'


class AppointmentForm(forms.ModelForm):

    class Meta:
        model = Appointment
        fields = ('name', 'email', 'date',)
        widgets = {
            'date': DateInput(),
        }

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )


class PostForm(forms.ModelForm):

    class Meta:
        model = Sell
        fields = ('seller', 'description','location','email','image0','image1','image2',)

'''
class WishlistForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ('wishlist',)
'''
class MaintenanceForm(forms.ModelForm):

    class Meta:
        model = Tenant
        fields = ['issues']

class PaymentForm(forms.ModelForm):
    Card_Number = forms.RegexField(regex="^(5[1-5][0-9]{14}|2(22[1-9][0-9]{12}|2[3-9][0-9]{13}|[3-6][0-9]{14}|7[0-1][0-9]{13}|720[0-9]{12}))$")
    CVV = forms.RegexField(regex = "^[0-9]{3}$")
    expiry = forms.RegexField(regex = "^(0[1-9]|1[0-2])\/?(([0-9]{4}|[0-9]{2})$)")

    class Meta:
        model = Tenant
        fields = ('Card_Number','CVV','expiry','due',)
class FilterForm(forms.ModelForm):
    class Meta:
        model = Filter
        fields = ('city','proptype','use',)

