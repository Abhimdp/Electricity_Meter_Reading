from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import MeterReading

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    bsl_staff_no = forms.CharField(max_length=10)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'bsl_staff_no')

class LoginForm(forms.Form):
    username = forms.CharField(label='Username')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

class LoginForm(AuthenticationForm):
    pass

class MeterReadingForm(forms.ModelForm):
    class Meta:
        model = MeterReading
        fields = ['staff_id', 'quarter_no', 'current_reading', 'previous_reading', 'meter_image']
        widgets = {
            'previous_reading': forms.TextInput(attrs={'value': '00000'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get('status')
        rejection_reason = cleaned_data.get('rejection_reason')

        if status == 'rejected' and not rejection_reason:
            self.add_error('rejection_reason', 'Please provide a rejection reason if the status is rejected.')

        return cleaned_data

class RejectionReasonForm(forms.Form):
    REJECTION_REASONS = [
        ('incorrect_image', 'Meter image not correct'),
        ('unclear_reading', 'Image reading not clear'),
        ('different_meter', 'Different meter'),
        ('wrong_reading', 'Inserting wrong reading')
    ]
    rejection_reason = forms.ChoiceField(
        choices=REJECTION_REASONS,
        label='Reason for Rejection'
    )
