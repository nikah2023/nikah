from sched import scheduler
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound

from django.utils.decorators import method_decorator
from django.views.generic import UpdateView
from django.contrib.auth.models import User
from django.urls import reverse_lazy

from django.urls import reverse

import datetime
import time

from django.db import models
from django.db.models import Q

# Подключение моделей
from .models import Person, Photo, Friend, Status, Message
# Подключение форм
from .forms import PersonForm, StatusForm, PhotoForm, SignUpForm

# Подключение моделей
from django.contrib.auth.models import User, Group, AnonymousUser
from django.contrib.auth import login as auth_login

# Create your views here.
# Групповые ограничения
def group_required(*group_names):
    """Requires user membership in at least one of the groups passed in."""
    def in_groups(u):
        if u.is_authenticated:
            if bool(u.groups.filter(name__in=group_names)) | u.is_superuser:
                return True
        return False
    return user_passes_test(in_groups, login_url='403')

# Стартовая страница 
def index(request):
    person = Person.objects.filter(okay=True).order_by('?')[0:4]   
    return render(request, "index.html", {"person": person, })    

# Контакты
def contact(request):
    return render(request, "contact.html")

# Кабинет
@login_required
def cabinet(request):   
    person = Person.objects.get(user_id=request.user.id)     
    my_status = Status.objects.filter(person_id=request.user.person.id).order_by('-dates').first()         
    return render(request, "cabinet.html", {"person": person, "my_status": my_status})

# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def person_index(request):
    person = Person.objects.all().order_by('user')
    return render(request, "person/index.html", {"person": person})

# Список для просмотра
def person_list(request):
    my_person = None
    my_status = None
    friend = None
    # Если это анонимный пользователь
    if request.user == AnonymousUser():
        person = Person.objects.filter(okay=True).order_by('?')
    else:
        # Если это пользователь которого нет в связанной таблице Person
        try:
            persons = Person.objects.get(user_id=request.user.id) 
        except Person.DoesNotExist:
            persons = None
        if (persons is None):
            person = Person.objects.filter(okay=True).order_by('user_id')
        else:
            # Себя в списке не показывать
            person_id = request.user.person.id
            person = Person.objects.filter(okay=True).exclude(id=person_id).order_by('?')
            friend = Friend.objects.filter(Q(person_id=person_id) | Q(amigo_id=person_id))
            my_person = request.user.person
            my_status = Status.objects.filter(person_id=request.user.person.id).order_by('-dates').first()     
            # Все друзья    
            #friends_query = Friend.objects.all()
            # Люди которые не с кем не дружат
            #person_not_friends = Person.objects.exclude(id__in=friends_query)
    return render(request, "person/list.html", {"person": person, "my_person": my_person, "my_status": my_status, "friend": friend, })

# Функция edit выполняет редактирование объекта.
# Функция в качестве параметра принимает идентификатор объекта в базе данных.
@login_required
#def person_edit(request, id):
def person_edit(request):
    try:
        id = request.user.person.id
        person = Person.objects.get(id=id) 
        my_person = person
        status = Status.objects.filter(person_id=id).order_by('-dates')     
        my_status = Status.objects.filter(person_id=id).order_by('-dates').first()  
        # Получить список национальностей для словаря
        nationality_list = Person.objects.order_by('nationality').values('nationality').distinct()
        marital_status_list = Person.objects.order_by('marital_status').values('marital_status').distinct()
        country_list = Person.objects.order_by('country').values('country').distinct()
        city_list = Person.objects.order_by('city').values('city').distinct()
        education_list = Person.objects.order_by('education').values('education').distinct()
        eye_color_list = Person.objects.order_by('eye_color').values('eye_color').distinct()
        hair_color_list = Person.objects.order_by('hair_color').values('hair_color').distinct()
        body_type_list = Person.objects.order_by('body_type').values('body_type').distinct()
        if request.method == "POST":
            person.sex = request.POST.get("sex")
            person.birthday = request.POST.get("birthday")
            person.nationality = request.POST.get("nationality")
            person.marital_status = request.POST.get("marital_status")
            person.amount_of_children = request.POST.get("amount_of_children")
            person.phone_number = request.POST.get("phone_number")
            person.email = request.POST.get("email")
            person.country = request.POST.get("country")
            person.city = request.POST.get("city")
            person.education = request.POST.get("education")
            person.occupation = request.POST.get("occupation")
            person.interests = request.POST.get("interests")
            person.eye_color = request.POST.get("eye_color")
            person.hair_color = request.POST.get("hair_color")
            person.body_type = request.POST.get("body_type")
            person.height = request.POST.get("height")
            person.weight = request.POST.get("weight")
            if "avatar" in request.FILES:                
                person.avatar = request.FILES["avatar"]
            personform = PersonForm(request.POST)
            if personform.is_valid():
                person.save()
                return HttpResponseRedirect(reverse('cabinet'))
            else:
                return render(request, "person/edit.html", {"form": personform})                
        else:
            # Загрузка начальных данных
            print(body_type_list)
            personform = PersonForm(initial={'sex': person.sex, 'birthday': person.birthday.strftime('%Y-%m-%d'), 'nationality': person.nationality, 'marital_status': person.marital_status, 
                                             'amount_of_children': person.amount_of_children, 'phone_number': person.phone_number, 'email': person.email, 'country': person.country, 
                                             'city': person.city, 'education': person.education, 'occupation': person.occupation, 'interests': person.interests, 
                                             'eye_color': person.eye_color, 'hair_color': person.hair_color, 'body_type': person.body_type, 'height': person.height, 
                                             'weight': person.weight, 'avatar': person.avatar})
            return render(request, "person/edit.html", {"form": personform, "my_person": my_person,"my_status": my_status, "status": status, 'nationality_list': nationality_list, 
                                                        'marital_status_list': marital_status_list, 'country_list': country_list, 'city_list': city_list,
                                                        'education_list': education_list, 'eye_color_list': eye_color_list, 'hair_color_list': hair_color_list,
                                                       'body_type_list': body_type_list})
    except Person.DoesNotExist:
        return HttpResponseNotFound("<h2>Person not found</h2>")

# Просмотр страницы read.html для просмотра объекта.
@login_required
def person_read(request, id):
    # id текущего пользователя
    # id user текущего пользователя
    my_user_id = request.user.id
    try:
        my_person_id = request.user.person.id
    except:
        my_person_id = None
    try:
        person = Person.objects.get(id=id)
        # id пользователя котрому отправляется сообщение
        person_user_id = person.user.id    
        my_friend = Friend.objects.filter(Q(confirmation=True), Q(person_id=my_person_id) | Q(amigo_id=my_person_id))  
        is_my_friend = Friend.objects.filter(Q(person_id=my_person_id) , Q(amigo_id=id)) | Friend.objects.filter( Q(person_id=id) , Q(amigo_id=my_person_id))  
        print("is_my_friend", is_my_friend)
        friend = Friend.objects.filter(Q(confirmation=True), Q(person_id=id) | Q(amigo_id=id))
        status = Status.objects.filter(person_id=id).order_by('-dates')
        status_last = Status.objects.filter(person_id=id).order_by('-dates').first()
        photo = Photo.objects.filter(person_id=id).order_by('-datep')
        message = Message.objects.filter(Q(sender_id=my_user_id) | Q(recipient_id=my_user_id)).filter(Q(sender_id=person_user_id) | Q(recipient_id=person_user_id)).order_by('-datem')
        if request.method == "POST":
            mes = Message()
            mes.sender_id = my_user_id
            mes.recipient_id = person_user_id
            mes.details = request.POST.get("message")
            mes.save()
            return HttpResponseRedirect(reverse('person_read', args=(id,)))
        else:
            print("id", id)
            print("my_person_id", my_person_id)
            return render(request, "person/read.html", {"person": person,  "status_last": status_last, "message": message, "status": status, "photo": photo, "my_user_id": my_user_id, "my_person_id":  my_person_id, "person_id": id,"friend": friend, "my_friend": my_friend, "is_my_friend": is_my_friend })
            #return render(request, "person/read.html", {"person": person, "my_person": my_person, "my_status": my_status, "status_last": status_last, "message": message, "friend": friend, "my_friend": my_friend, "status": status, "photo": photo, "my_id": my_id, "person_id": id })
    except Person.DoesNotExist:
        return HttpResponseNotFound("<h2>Person not found</h2>")

# Подтверждение персоны
@login_required
@group_required("Managers")
def person_okay(request, id):
    try:
        person = Person.objects.get(id=id)
        person.okay = True
        person.save()
        return HttpResponseRedirect(reverse('person_index'))
    except Person.DoesNotExist:
        return HttpResponseNotFound("<h2>Person not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def friend_index(request):
    friend = Friend.objects.all().order_by('-datef')
    return render(request, "friend/index.html", {"friend": friend})

# Список для просмотра
@login_required
def friend_list(request):
    # id текущего пользователя
    my_id = request.user.person.id
    my_person = request.user.person
    my_status = Status.objects.filter(person_id=request.user.person.id).order_by('-dates').first() 
    # Друзья текущего пользователя
    friend = Friend.objects.filter(Q(person_id=my_id) | Q(amigo_id=my_id))
    return render(request, "friend/list.html", {"friend": friend, "my_id": my_id, "my_person": my_person, "my_status": my_status})

# Подтверждение дружбы
@login_required
def friend_confirm(request, id):
    friend = Friend.objects.get(id=id)
    friend.confirmation = True
    friend.save()
    return HttpResponseRedirect(reverse('friend_list'))

@login_required
def friend_create(request, id):
    friend = Friend()
    friend.person_id = request.user.person.id
    friend.amigo_id = id
    friend.save()
    return HttpResponseRedirect(reverse('person_list'))

# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def status_index(request):
    status = Status.objects.all().order_by('-dates')
    return render(request, "status/index.html", {"status": status})

@login_required
def status_list(request):
    status = Status.objects.filter(person_id=request.user.person.id).order_by('-dates')
    my_person = request.user.person
    my_status = Status.objects.filter(person_id=request.user.person.id).order_by('-dates').first()         
    return render(request, "status/list.html", {"status": status, "my_person": my_person, "my_status": my_status})

# В функции create() получаем данные из запроса типа POST, сохраняем данные с помощью метода save()
# и выполняем переадресацию на корень веб-сайта (то есть на функцию index).
@login_required
def status_create(request):
    if request.method == "POST":
        status = Status()        
        status.person_id = request.user.person.id
        status.title = request.POST.get("title")
        status.save()
        return HttpResponseRedirect(reverse('cabinet'))
    else:
        statusform = StatusForm()
        return render(request, "status/create.html", {"form": statusform})

# Функция edit выполняет редактирование объекта.
# Функция в качестве параметра принимает идентификатор объекта в базе данных.
@login_required
def status_edit(request, id):
    try:
        status = Status.objects.get(id=id) 
        if request.method == "POST":
            status.title = request.POST.get("title")
            status.save()
            return HttpResponseRedirect(reverse('cabinet'))
        else:
            # Загрузка начальных данных
            statusform = StatusForm(initial={'title': status.title,  })
            return render(request, "status/edit.html", {"form": statusform})
    except Status.DoesNotExist:
        return HttpResponseNotFound("<h2>Status not found</h2>")

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
def status_delete(request, id):
    try:
        status = Status.objects.get(id=id)
        status.delete()
        return HttpResponseRedirect(reverse('cabinet'))
    except Status.DoesNotExist:
        return HttpResponseNotFound("<h2>Status not found</h2>")

# Просмотр страницы read.html для просмотра объекта.
@login_required
def status_read(request, id):
    try:
        status = Status.objects.get(id=id) 
        return render(request, "status/read.html", {"status": status})
    except Status.DoesNotExist:
        return HttpResponseNotFound("<h2>Status not found</h2>")

# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def message_index(request):
    message = Message.objects.all().order_by('-datem')
    return render(request, "message/index.html", {"message": message})

# Регистрационная форма 
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            # Добавить профиль
            person = Person()
            person.user = user
            person.sex = "Ж"
            person.birthday = datetime.datetime.now()
            person.nationality = "Казашка"
            person.marital_status = "Не замужем"
            person.country = "Казахстан"
            person.city = "Алматы"
            person.amount_of_children = 0
            person.height = 0
            person.weight = 0
            person.save()
            person = Person.objects.all().order_by("-id")[0]
            #print(person)
            #print(person.id)            
            return redirect('person_edit')
            return redirect('index')
            #return render(request, 'registration/register_done.html', {'new_user': user})
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

@method_decorator(login_required, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    fields = ('first_name', 'last_name', 'email',)
    template_name = 'registration/my_account.html'
    success_url = reverse_lazy('index')
    #success_url = reverse_lazy('my_account')
    def get_object(self):
        return self.request.user


