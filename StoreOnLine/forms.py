from django import forms
from django.contrib.auth.models import User

#from users.models import User

class RegisterForm(forms.Form):
    username = forms.CharField(required=True, min_length=4, max_length=50,
                                widget=forms.TextInput(attrs={
                                'class':'form-control', 'id':'username'
                                }))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
                                'class':'form-control', 'id':'email',
                                'placeholder':'example@misena.edu.co'
                                }))
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={
                                'class':'form-control'
                                }))
    password2 = forms.CharField(label='Confirmar Password', required=True,
                                widget=forms.PasswordInput(attrs={
                                'class':'form-control'
                                }))

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('El username ya se encuentra registrado')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('El email ya se encuentra registrado')
        return email

    def clean(self):
        #utilizamos el metodo clean de nuestra clase padre
        cleaned_data = super().clean()
        if cleaned_data.get('password2') != cleaned_data.get('password'):
            #add_error recibe dos argumentos el primero es el campo al cual le queremos agregar ese error
            #El segundo argumento es el mensaje de error
            self.add_error('password2', 'Los password no coinciden')

    def save(self):
        #create_user nos retorna un objeto de tipo user con tres paramentros
        return User.objects.create_user(
            self.cleaned_data.get('username'),
            self.cleaned_data.get('email'),
            self.cleaned_data.get('password'),
        )
