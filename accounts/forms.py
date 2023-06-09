from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                                    'style': 'font-size: large'}))
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                                            'style': 'font-size: large'}))

    class Meta:
        model = get_user_model()
        fields = (
            'email', 'first_name', 'last_name', 'mobile_nr', 'pesel')

    def clean_password2(self):
        """Check if the two password entries match"""
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Hasła nie są zgodne")
        return password2

    def save(self, commit=True):
        """Save the provided password in hashed format"""
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = get_user_model()
        fields = (
            'email', 'first_name', 'last_name', 'mobile_nr', 'pesel', 'is_active', 'is_admin', 'is_staff')


class LoginForm(AuthenticationForm):
    username = forms.EmailField(max_length=100,
                                required=True,
                                widget=forms.TextInput(attrs={'placeholder': 'e-mail',
                                                              'class': 'form-control',
                                                              'style': 'font-size: large'
                                                              }))
    password = forms.CharField(max_length=50,
                               required=True,
                               widget=forms.PasswordInput(attrs={'placeholder': 'Hasło',
                                                                 'class': 'form-control',
                                                                 'id': 'password',
                                                                 'name': 'password',
                                                                 'style': 'font-size: large'
                                                                 }))

    class Meta:
        model = get_user_model()
        fields = ['username', 'password']
