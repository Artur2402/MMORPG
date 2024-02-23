from allauth.account.forms import SignupForm
from django import forms
from django.contrib.auth.models import User, Group


class EditProfile(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username',
                  'email',
                  'first_name',
                  'last_name')


class Auth_codeForm(forms.Form):
    code = forms.IntegerField(label="Код регистрации")


class BasicSignUpForm(SignupForm):

    def save(self, request):
        user = super().save(request)
        user.save()
        return user
