from django.shortcuts import render, redirect
from django.db.models import Q
from .models import Room, RoomGame
from .forms import RoomForm
# Create your views here.

# rooms = [
#     {'id': 1, 'name': 'Fortnite'},
#     {'id': 2, 'name': 'DotA 2'},
#     {'id': 3, 'name': 'Monster Hunter'},
# ]

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(game__name__contains=q) |
        Q(name__contains=q) |
        Q(description__contains=q)
        )
    
    games = RoomGame.objects.all()
    room_count = rooms.count()
    context = {'rooms': rooms, 'games': games, 'room_count':room_count}
    return render(request, 'base/home.html', context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    context = {'room' : room}
    return render(request, 'base/room.html', context)

def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'base/room_form.html', context)

def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.method == 'POST':
        form = RoomForm(request.POST, instance = room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/room_form.html', context)

def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    context = {'object': room}
    return render(request, 'base/delete.html', context)