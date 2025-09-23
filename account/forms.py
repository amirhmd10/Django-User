from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

from .models import Profile


User = get_user_model()

class UserSignUpForm(forms.ModelForm):
    password1= forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter password'}) ,
        label='Password'
    )
    password2= forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm password'}) ,
        label='Password confirmation'
    )

    class Meta:
        model = User
        fields = ['username','email']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Enter username'}) ,
            'email': forms.TextInput(attrs={'placeholder': 'Enter email'}) ,
        }

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        validate_password(password1, self.instance)
        return password1

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get("password1")
        p2 = cleaned_data.get("password2")
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("passwords don't match")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user




class UserLoginForm(forms.Form):
    username_or_Email = forms.CharField(
        label='Username or Email' ,
        widget=forms.TextInput(attrs={'placeholder': 'Username or Email'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),
        label='password'
    )

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        if not email or not password:
            raise forms.ValidationError("Invalid email or password")
        return cleaned_data


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name','last_name', 'bio' , 'avatar', 'phone_number']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'First name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last name'}),
            'bio': forms.Textarea(attrs={'placeholder': 'Write something…'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Phone number'}),
        }





# این گونه هم می توان دخیره کرد فقط این گونه پیاده سازی به صورت clear text ذخیره میکند.
        # def clean(self):
        #     cleaned_date = super().clean()
        #     if cleaned_date.get("password1") != cleaned_date.get("password2"):
        #         raise forms.ValidationError("Password Not Same.")
        #     return cleaned_date

