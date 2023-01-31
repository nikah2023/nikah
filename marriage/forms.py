from datetime import datetime
from django import forms
from django.forms import ModelForm, TextInput, Textarea, DateInput, DateTimeInput, NumberInput, CheckboxInput
from .models import Person, Photo, Status, Message
#from django.utils.translation import ugettext as _
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from dateutil.relativedelta import relativedelta
from django.utils import timezone

# При разработке приложения, использующего базу данных, чаще всего необходимо работать с формами, которые аналогичны моделям.
# В этом случае явное определение полей формы будет дублировать код, так как все поля уже описаны в модели.
# По этой причине Django предоставляет вспомогательный класс, который позволит вам создать класс Form по имеющейся модели
# атрибут fields - указание списка используемых полей, при fields = '__all__' - все поля
# атрибут widgets для указания собственный виджет для поля. Его значением должен быть словарь, ключами которого являются имена полей, а значениями — классы или экземпляры виджетов.

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ('sex', 'birthday', 'nationality', 'marital_status', 'amount_of_children', 'phone_number', 'email', 'country', 'city', 'education',  'occupation', 'interests', 'eye_color', 'hair_color', 'body_type', 'height', 'weight', 'avatar')
        widgets = {
            'birthday': DateInput(attrs={"type":"date"}),
            'nationality': TextInput(attrs={"size":"100", "required list": "nationality_datalist", "autocomplete":"on" }),
            'marital_status': TextInput(attrs={"size":"100", "required list": "marital_status_datalist", "autocomplete":"on" }),
            'amount_of_children': NumberInput(attrs={"size":"10"}),  
            'phone_number': TextInput(attrs={"size":"100", "type":"tel", "pattern": "+7-[0-9]{3}-[0-9]{3}-[0-9]{4}"}),
            'email': TextInput(attrs={"size":"100", "type":"email", "pattern": "[^@\s]+@[^@\s]+\.[^@\s]+"}),
            'country': TextInput(attrs={"size":"100", "required list": "country_datalist", "autocomplete":"on" }),
            'city': TextInput(attrs={"size":"100", "required list": "city_datalist", "autocomplete":"on" }),
            'education': TextInput(attrs={"size":"100", "required list": "education_datalist", "autocomplete":"on" }),
            'occupation': Textarea(attrs={'cols': 80, 'rows': 3}),            
            'interests': Textarea(attrs={'cols': 80, 'rows': 3}), 
            'eye_color': TextInput(attrs={"size":"100", "required list": "eye_color_datalist", "autocomplete":"on" }),
            'hair_color': TextInput(attrs={"size":"100", "required list": "hair_color_datalist", "autocomplete":"on" }),
            'body_type': TextInput(attrs={"size":"100", "required list": "body_type_datalist", "autocomplete":"on" }),
            'height': NumberInput(attrs={"size":"10"}),  
            'weight': NumberInput(attrs={"size":"10"}),              
        }
    # Метод-валидатор для поля birthday
    def clean_birthday(self):        
        if isinstance(self.cleaned_data['birthday'], datetime) == True:
            data = self.cleaned_data['birthday']
            # Проверка даты рождения не моложе 16 лет
            if data > timezone.now() - relativedelta(years=16):
                raise forms.ValidationError(_('Minimum age 16 years old'))
        else:
            raise forms.ValidationError(_('Wrong date and time format'))
        # Метод-валидатор обязательно должен вернуть очищенные данные, даже если не изменил их
        return data    
    # Метод-валидатор для поля height
    def clean_height(self):
        data = self.cleaned_data['height']
        #print(data)
        # Проверка больше нуля
        if data <= 0:
            raise forms.ValidationError(_('Height must be greater than zero'))
        # Проверка в диапазоне
        if (data < 50) or (data > 300):
            raise forms.ValidationError(_('Height should not be less than 50 or more than 300'))
        # Метод-валидатор обязательно должен вернуть очищенные данные, даже если не изменил их
        return data
    # Метод-валидатор для поля weight
    def clean_weight(self):
        data = self.cleaned_data['weight']
        #print(data)
        # Проверка больше нуля
        if data <= 0:
            raise forms.ValidationError(_('Weight must be greater than zero'))
        # Проверка в диапазоне
        if (data < 20) or (data > 300):
            raise forms.ValidationError(_('Weight should not be less than 20 or more than 300'))
        # Метод-валидатор обязательно должен вернуть очищенные данные, даже если не изменил их
        return data        



class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ('title',)
        widgets = {
            'title': TextInput(attrs={"size":"100"}),            
        }

class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ('title', 'snapshot')
        widgets = {
            'title': TextInput(attrs={"size":"100"}),            
        }

# Форма регистрации
class SignUpForm(UserCreationForm):
    email = forms.CharField(max_length=254, required=True, widget=forms.EmailInput())
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'first_name', 'last_name', 'email')