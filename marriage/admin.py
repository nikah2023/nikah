from django.contrib import admin

from .models import Person, Photo, Friend, Status, Message

# Добавление модели на главную страницу интерфейса администратора
admin.site.register(Person)
admin.site.register(Photo)
admin.site.register(Friend)
admin.site.register(Status)
admin.site.register(Message)