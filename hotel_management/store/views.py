from django.shortcuts import render,get_object_or_404
from .models import Room, RoomType

from service.models import MealCode

def room_all(request):
    rooms = Room.rooms.all()
    return render(request, 'room/room_all.html', {'rooms':rooms})

def room_detail(request, slug):
    room = get_object_or_404(Room, slug=slug)
    room_type = get_object_or_404(RoomType, id=room.room_type_id.id)
    meal_codes = MealCode.objects.all()
    adult_selected_list = list(range(1,int(room_type.max_adult)+1))
    child_selected_list = list(range(1,int(room_type.max_child)+1))
    return render(request, 'room/room_detail.html', {'room':room, 'room_type':room_type, 'adult_selected_list':adult_selected_list, 'child_selected_list':child_selected_list, 'meal_codes':meal_codes})

# service and service detail
def service(request):
    context = {}
    return render(request, 'service/service.html', context)

def service_meal(request):
    meal_codes = MealCode.objects.all()
    return render(request, 'service/service_meal.html', {'meal_codes':meal_codes})

def home(request):
    context = {}
    return render(request, 'home.html', context)

def about(request):
    context = {}
    return render(request, 'about.html', context)


def team(request):
    context = {}
    return render(request, 'team.html', context)

# def booking(request):
#     context = {}
#     return render(request, 'booking.html', context)

def contact(request):
    context = {}
    return render(request, 'contact.html', context)

def testimonial(request):
    context = {}
    return render(request, 'testimonial.html', context)
