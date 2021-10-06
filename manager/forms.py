from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.forms import BaseModelFormSet
from .models import Disk


class DiskForm(forms.ModelForm):
    
    class Meta:
        model = Disk
        fields = ('name', 'size', 'mount_point', 'mount_state', 'format')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].disabled = True
        self.fields['size'].disabled = True


    def clean_mount_point(self):
        mount_point = self.cleaned_data['mount_point']

        if mount_point == None or not mount_point.startswith('/'): 
            raise ValidationError('Имя точки монтирования должно начинаться с "/"')

        if mount_point == '/':
            raise ValidationError('Имя точки монтирования не может быть корневым каталогом')

        return mount_point


    def clean(self):
        cleaned_data = super().clean()
        mount_point = cleaned_data.get('mount_point')
        mount_state = cleaned_data.get('mount_state')
        name = cleaned_data.get('name')

        if mount_point and mount_state and name:

            disk = Disk.objects.get(name=name)
        
            if mount_state == 'umount' and mount_point != disk.mount_point:
                raise ValidationError(f'Укажите предыдущую точку монтирования: {disk.mount_point}')




class UserRegistrationForm(forms.ModelForm):
    """Форма регистрации пользователей"""
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password',
                                widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают')
        return cd['password2']
