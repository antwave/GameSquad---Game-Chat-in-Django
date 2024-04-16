from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Room, Game, Message
from .forms import RoomForm, UserForm


def loginView(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username = username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password incorrect')


    context = {'page': page}
    return render(request, 'base/login_register.html', context)

def logoutView(request):
    logout(request)
    return redirect('home')

def registerView(request):
    page = 'register'
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid registration')


    context = {'page': page, 'form': form}
    return render(request, 'base/login_register.html', context)

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(game__name__contains=q) |
        Q(name__contains=q) |
        Q(description__contains=q)
        )
    
    games = Game.objects.all()[0:5]
    room_count = rooms.count()

    sent_messages = Message.objects.filter(Q(room__game__name__icontains=q))

    context = {'rooms': rooms, 'games': games,
                'room_count':room_count, 'sent_messages':sent_messages}
    return render(request, 'base/home.html', context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()
    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    context = {'room' : room, 'room_messages': room_messages, 'participants':participants}
    return render(request, 'base/room.html', context)

def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    user_messages = user.message_set.all()
    games = Game.objects.all()
    context = {'user':user, 'rooms':rooms,
               'games': games, 'sent_messages':user_messages}
    return render(request, 'base/user_profile.html', context)

@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    games = Game.objects.all()
    if request.method == 'POST':
        game_name = request.POST.get('game')
        game, created = Game.objects.get_or_create(name=game_name)
        Room.objects.create(
            host=request.user,
            game=game,
            name = request.POST.get('name'),
            description = request.POST.get('description')
        )
        return redirect('home')
    context = {'form': form, 'games':games}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    games = Game.objects.all()
    if request.user != room.host:
        return HttpResponse('Only the room host can edit the room')

    if request.method == 'POST':
        game_name = request.POST.get('game')
        game, created = Game.objects.get_or_create(name=game_name)
        room.name = request.POST.get('name')
        room.game = game
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')

    context = {'form': form, 'games':games, 'room': room}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('Only the room host can delete the room')

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    context = {'object': room}
    return render(request, 'base/delete.html', context)

@login_required(login_url='login')
def deleteMessage(request, pk):
    msg = Message.objects.get(id=pk)

    if request.user != msg.user:
        return HttpResponse('Only the room host can delete the room')

    if request.method == 'POST':
        room_id = msg.room.id
        msg.delete()
        return redirect('home')
    context = {'object': msg}
    return render(request, 'base/delete.html', context)

@login_required(login_url='login')
def editUser(request):
    user = request.user 
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk = user.id)
    return render(request, 'base/edit-user.html', {'form': form})

def gamesPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    games = Game.objects.filter(name__icontains=q)
    context = {'games': games}
    return render(request, 'base/games.html', context)

def activityPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    sent_messages = Message.objects.filter(Q(room__game__name__icontains=q))
    context = {'sent_messages': sent_messages}
    return render(request, 'base/activity.html', context)

# TODO:
#     - Fix delete message routing
#     - Remove user from conversation when last message is deleted