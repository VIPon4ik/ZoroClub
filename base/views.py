from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.db.models import Count, Q
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .forms import AnnouncmentForm, MyUserCreationForm
from .models import Announcment, Breed, Sex, Purpose, City, User, Chat, Message



def home(request):
    purpose = request.GET.get('purpose') if request.GET.get('purpose') != None else ''
    city = request.GET.get('city') if request.GET.get('city') != None else ''
    breed = request.GET.get('breed') if request.GET.get('breed') != None else ''
    sex = request.GET.get('sex') if request.GET.get('sex') != None else ''
    if request.method == 'GET':
        print(breed,city,purpose,sex);
    announcments = Announcment.objects.exclude(~Q(breed__name__icontains=breed)|
                                              ~Q(city__name__icontains=city)|
                                              ~Q(purpose__name__icontains=purpose)|
                                               ~Q(sex__name__icontains=sex))
    cities = City.objects.all()
    breeds = Breed.objects.all()
    purposes = Purpose.objects.all()
    context = {'announcments':announcments,'cities':cities,'breeds':breeds, 'purposes':purposes,
               'selected_breed':breed,'selected_city':city,'selected_purpose':purpose}
    return render(request,'base/home.html', context)

def announcment(request,pk):
    announcment = Announcment.objects.get(id=pk)
    context = {'announcment':announcment}
    return render(request, 'base/announcment.html', context)

@login_required(login_url='login')
def createAnnouncment(request):
    page = 'create'
    cities = City.objects.all()
    breeds = Breed.objects.all()
    purposes = Purpose.objects.all()
    form = AnnouncmentForm()
    if request.method == 'POST':
        # if request.FILES.get('image') == '':
        #     messages.error(request,'Загрузіть фотографію улюбленця!')
        breed_name = request.POST.get('breed') if request.POST.get('breed') != '' else ''
        breed, created = Breed.objects.get_or_create(name=breed_name)
        sex_name = request.POST.get('sex') if request.POST.get('sex') != '' else '-'
        sex, created = Sex.objects.get_or_create(name=sex_name)
        purpose_name = request.POST.get('purpose') if request.POST.get('purpose') != '' else '-'
        purpose, created = Purpose.objects.get_or_create(name=purpose_name)
        city_name = request.POST.get('city') if request.POST.get('city') != '' else '-'
        city, created = City.objects.get_or_create(name=city_name)

        if request.FILES.get('image') == None:
            messages.error(request, 'Виберіть фотографію')
            return redirect('create-announcment')
        else:
            Announcment.objects.create(
                owner = request.user,
                name = request.POST.get('name'),
                breed=breed,
                old=request.POST.get('old'),
                sex=sex,
                documents=request.POST.get('documents') if request.POST.get('documents') != '' else '-',
                purpose=purpose,
                city=city,
                description=request.POST.get('description') if request.POST.get('description') != '' else '-',
                price=request.POST.get('price'),
                image=request.FILES.get('image'),
            )

        return redirect('home')
    context = {'form':form, 'page':page,'cities':cities, 'breeds':breeds, 'purposes':purposes}
    return render(request, 'base/create-announcment.html', context)

@login_required(login_url='login')
def updateAnnouncment(request,pk):
    announcment = Announcment.objects.get(id=pk)
    cities = City.objects.all()
    breeds = Breed.objects.all()
    purposes = Purpose.objects.all()

    if request.user != announcment.owner:
        return HttpResponse('You are not allowed here!!')
    if request.method == 'POST':
        breed_name = request.POST.get('breed') if request.POST.get('breed') != '' else '-'
        breed, created = Breed.objects.get_or_create(name=breed_name)
        sex_name = request.POST.get('sex') if request.POST.get('sex') != '' else '-'
        sex, created = Sex.objects.get_or_create(name=sex_name)
        purpose_name = request.POST.get('purpose') if request.POST.get('purpose') != '' else '-'
        purpose, created = Purpose.objects.get_or_create(name=purpose_name)
        city_name = request.POST.get('city') if request.POST.get('city') != '' else '-'
        city, created = City.objects.get_or_create(name=city_name)

        announcment.name = request.POST.get('name')
        announcment.breed = breed
        announcment.old = request.POST.get('old')
        announcment.sex = sex
        announcment.documents = request.POST.get('documents') if request.POST.get('documents') != '' else '-'
        announcment.purpose = purpose
        announcment.city = city
        announcment.description = request.POST.get('description') if request.POST.get('description') != '' else '-'
        announcment.price = request.POST.get('price')

        announcment.save()
        return redirect('announcment',announcment.id)

    context = {'announcment':announcment,'cities':cities,'breeds':breeds,'purposes':purposes}
    return render(request, 'base/update-announcment.html', context)

@login_required(login_url='login')
def deleteAnnouncment(request, pk):
    announcment = Announcment.objects.get(id=pk)
    if announcment.owner != request.user:
        return redirect('home')
    if request.method == 'POST':
        announcment.delete()
        return redirect('home')
    return render(request,'base/delete.html', {'obj':announcment})

def registerPage(request):
    page = 'register'
    if request.method == 'POST':
        if request.POST.get('password1') == request.POST.get('password2'):
            if request.POST.get('check'):
                if len(request.POST.get('password1')) >= 8:
                    email = request.POST.get('email')
                    try:
                        User.objects.get(email=email)
                        messages.error(request,'Такий користувач вже існує')
                    except:
                        User.objects.create_user(
                            username=request.POST.get('email'),
                            email=email,
                            password=request.POST.get('password1'),
                            city=City.objects.get(name='Інше'),
                            number='380'
                        )
                        return redirect('login')
                else:
                    messages.error(request, 'Пароль має бути не менше 8 символів')
            else:
                messages.error(request, 'Ви не погодились з правилами')
        else:
            messages.error(request,'Паролі не співпадають')
    context = {'page':page}
    return render(request,'base/log_reg.html', context)

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request,'Користувача не існує')
            return redirect('login')

        user = authenticate(request, email=email, password = password)

        if user is not None:
            if request.POST.get('check'):
                login(request, user)
                return redirect('home')
            else:
                messages.error(request,'Ви не погодились з правилами')
        else:
            messages.error(request,'Пароль невірний')
    return render(request,'base/log_reg.html', {'page':page})

def logoutPage(request):
    logout(request)
    return redirect('home')

def profilePage(request, pk):
    page = 'profile'
    user = User.objects.get(id=pk)
    announcments = Announcment.objects.filter(owner=user)
    return render(request, 'base/profile.html', {'user':user, 'page':page,'announcments':announcments})

@login_required(login_url='login')
def editProfile(request):
    user = request.user
    cities = City.objects.all()
    if request.method == 'POST':
        city_name = request.POST.get('city') if request.POST.get('city') != '' else 'Інше'
        city, created = City.objects.get_or_create(name=city_name)

        user.username = request.POST.get('username')
        user.city = city
        if request.FILES.get('avatar') != None:
            user.avatar = request.FILES.get('avatar')

        if len(request.POST.get('number')) > 9 and len(request.POST.get('number')) < 14:
            user.number = request.POST.get('number').replace('-','')
            user.save()
        else:
            messages.error(request,'Номер має складатись мінімум з 9 цифр, але не більше 13')
            return redirect('edit-profile')

        return redirect('profile',user.id)
    return render(request,'base/edit-profile.html', {'user':user,'cities':cities})

@login_required(login_url='login')
def favoritesPage(request):
    page = 'favorites'
    user = request.user
    announcments = Announcment.objects.filter(favorites=user)
    context = {'announcments':announcments, 'page':page}
    return render(request,'base/favorites.html',context)

@login_required(login_url='login')
def favoritesAdd(request,pk):
    page = request.META.get('HTTP_REFERER')
    announcment = Announcment.objects.get(id=pk)
    announcment.favorites.add(request.user)
    return redirect(page)

@login_required(login_url='login')
def favoritesDelete(request,pk):
    page = request.META.get('HTTP_REFERER')
    announcment = Announcment.objects.get(id=pk)
    announcment.favorites.remove(request.user)
    return redirect(page)

@login_required(login_url='login')
def chatPanel(request):
    page = 'chat-panel'
    users = User.objects.all()
    chats_in = Chat.objects.filter(participants=request.user).order_by('-updated')
    context = {'page':page, 'chats_in':chats_in, 'users':users}
    return render(request,'base/chat.html',context)

@login_required(login_url='login')
def createChat(request,user_id):
    user2 = User.objects.get(id=user_id)
    if int(user_id) == request.user.id:
        return redirect('chat-panel')
    if Chat.objects.annotate(num_participants=Count('participants')).filter(participants=request.user).filter(participants=user2).filter(num_participants=2).first():
        return redirect('chat-panel')
    else:
        user1 = request.user
        chat = Chat(user_id=user_id)
        chat.save()
        chat.participants.add(user1,user2)
        chat.save()
        return redirect('chat-page',user_id)

@login_required(login_url='login')
def chatPage(request,pk):
    page = 'chat'
    user = User.objects.get(id=pk)
    chats_in = Chat.objects.filter(participants=request.user).order_by('-updated')
    chat = Chat.objects.annotate(num_participants=Count('participants')).filter(participants=request.user).filter(participants=user).filter(num_participants=2).first()
    messages = Message.objects.filter(chat=chat)
    if request.method == 'POST':
        body = request.POST.get('body')
        if body == '':
            print()
        else:
            Message.objects.create(
                chat = chat,
                body = request.POST.get('body'),
                user = request.user,
            )
            chat.updated = timezone.now()
            chat.save()
    context = {'chat': chat, 'messages':messages,'chats_in':chats_in,'our_user':user, 'page':page}
    return render(request, 'base/chat.html', context)



