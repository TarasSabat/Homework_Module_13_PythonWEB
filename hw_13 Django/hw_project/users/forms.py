from quotes.models import Author, Quote
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}),
                               label='Username',
                               help_text='Required. 100 characters or fewer. Letters, digits and @/./+/-/_ only.')

    email = forms.CharField(max_length=100,
                            required=True,
                            widget=forms.TextInput(),
                            label='Email'
                            )

    password1 = forms.CharField(max_length=50,
                                required=True,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                label='Password',
                                help_text='Your password must contain at least 8 characters.')

    password2 = forms.CharField(max_length=50,
                                required=True,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                label='Confirm Password',
                                help_text='Enter the same password as before, for verification.')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ('fullname', 'born_date', 'born_location', 'description')
        labels = {
            'fullname': 'Full Name',
            'born_date': 'Born Date',
            'born_location': 'Born Location',
            'description': 'Description',
        }


class QuoteForm(forms.ModelForm):
    author_fullname = forms.CharField(max_length=50, required=False)

    class Meta:
        model = Quote
        fields = ['quote', 'tags', 'author_fullname']

    def save(self, commit=True):
        author_fullname = self.cleaned_data['author_fullname']
        quote = super().save(commit=False)
        if author_fullname:
            author, created = Author.objects.get_or_create(fullname=author_fullname)
            quote.author = author
        if commit:
            quote.save()
        return quote