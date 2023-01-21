from django.db import models
#from django.utils.translation import ugettext as _
from django.utils.translation import gettext_lazy as _

from PIL import Image
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
from django.core.files.storage import default_storage as storage  

from django.contrib.auth.models import User

# Модели отображают информацию о данных, с которыми вы работаете.
# Они содержат поля и поведение ваших данных.
# Обычно одна модель представляет одну таблицу в базе данных.
# Каждая модель это класс унаследованный от django.db.models.Model.
# Атрибут модели представляет поле в базе данных.
# Django предоставляет автоматически созданное API для доступа к данным

# choices (список выбора). Итератор (например, список или кортеж) 2-х элементных кортежей,
# определяющих варианты значений для поля.
# При определении, виджет формы использует select вместо стандартного текстового поля
# и ограничит значение поля указанными значениями.

# Читабельное имя поля (метка, label). Каждое поле, кроме ForeignKey, ManyToManyField и OneToOneField,
# первым аргументом принимает необязательное читабельное название.
# Если оно не указано, Django самостоятельно создаст его, используя название поля, заменяя подчеркивание на пробел.
# null - Если True, Django сохранит пустое значение как NULL в базе данных. По умолчанию - False.
# blank - Если True, поле не обязательно и может быть пустым. По умолчанию - False.
# Это не то же что и null. null относится к базе данных, blank - к проверке данных.
# Если поле содержит blank=True, форма позволит передать пустое значение.
# При blank=False - поле обязательно.

# Персона (человек)
class Person(models.Model):
    SEX_CHOICES = (
        ('М','М'),
        ('Ж', 'Ж'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    sex = models.CharField(_('sex'), max_length=1, choices=SEX_CHOICES, default='М')
    birthday = models.DateTimeField(_('birthday'))    
    nationality = models.CharField(_('nationality'), max_length=64)
    marital_status = models.CharField(_('marital_status'), max_length=64)
    amount_of_children = models.IntegerField(_('amount_of_children'))
    phone_number = models.CharField(_('phone_number'), max_length=64, blank=True, null=True)
    email = models.EmailField(_('email'), blank=True, null=True)
    country = models.CharField(_('country'), max_length=64)
    city = models.CharField(_('city'), max_length=64)    
    education = models.CharField(_('education'), max_length=64, blank=True, null=True)    
    occupation = models.TextField(_('person_occupation'), blank=True, null=True)
    interests = models.TextField(_('person_interests'), blank=True, null=True)
    eye_color = models.CharField(_('eye_color'), max_length=64, blank=True, null=True)
    hair_color = models.CharField(_('hair_color'), max_length=64, blank=True, null=True)
    body_type = models.CharField(_('body_type'), max_length=64, blank=True, null=True)
    height = models.IntegerField(_('height'), blank=True, null=True)
    weight = models.IntegerField(_('weight'), blank=True, null=True)
    #avatar = models.ImageField(_('avatar'), upload_to='images/',default='default.png', blank=True, null=True)
    avatar = models.ImageField(_('avatar'), upload_to='images/', blank=True, null=True)
    okay = models.BooleanField(default=False)
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'person'
        # indexes - список индексов, которые необходимо определить в модели
        indexes = [
            models.Index(fields=['user']),            
        ]
        # Сортировка по умолчанию
        ordering = ['user']        
    def __str__(self):
        # Вывод в тег Select
        return "{} ({})".format(self.user, self.user.first_name)
    @property
    def fio(self):
        # Возврат ФИО
        return '%s %s' % (self.user.first_name, self.user.last_name)

# Фотографии
class Photo(models.Model):
    person = models.ForeignKey(Person, related_name='photo_person', on_delete=models.CASCADE)
    datep = models.DateTimeField(_('datep'), auto_now_add=True)
    snapshot = models.ImageField(_('snapshot'), upload_to='images/')
    title = models.CharField(_('title_photo'), max_length=256)
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'photo'
        # indexes - список индексов, которые необходимо определить в модели
        indexes = [
            models.Index(fields=['person']),
            models.Index(fields=['datep']),
        ]
        # Сортировка по умолчанию
        ordering = ['-datep']        

## Друзья
#class Friend(models.Model):
#    datef = models.DateTimeField(_('datef'), auto_now_add=True)
#    confirmation = models.BooleanField(_('confirmation'), default = False)
#    person = models.ForeignKey(Person, related_name='friend_person', on_delete=models.CASCADE)
#    amigo = models.ForeignKey(Person, related_name='amigo_person', on_delete=models.CASCADE)
#    class Meta:
#        # Параметры модели
#        # Переопределение имени таблицы
#        db_table = 'friend'
#        # indexes - список индексов, которые необходимо определить в модели
#        indexes = [
#            models.Index(fields=['person']),
#        ]
#        # Сортировка по умолчанию
#        #ordering = ['-datep']  

# Статус
class Status(models.Model):
    person = models.ForeignKey(Person, related_name='status_person', on_delete=models.CASCADE)
    dates = models.DateTimeField(_('dates'), auto_now_add=True)
    title = models.CharField(_('title_status'), max_length=256)
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'status'
        # indexes - список индексов, которые необходимо определить в модели
        indexes = [
            models.Index(fields=['person']),
            models.Index(fields=['dates']),
        ]
        # Сортировка по умолчанию
        ordering = ['-dates']

# Сообщения 
class Message(models.Model):
    datem = models.DateTimeField(_('datem'), auto_now_add=True)
    sender = models.ForeignKey(User, related_name='sender_message', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='recipient_message', on_delete=models.CASCADE)
    details = models.TextField(_('message_details'), blank=True, null=True)
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'message'
        # indexes - список индексов, которые необходимо определить в модели
        indexes = [
            models.Index(fields=['sender']),
            models.Index(fields=['recipient']),
        ]
        # Сортировка по умолчанию
        ordering = ['-datem']

