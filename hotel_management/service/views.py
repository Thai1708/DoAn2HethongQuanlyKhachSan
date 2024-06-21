from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import LaundryItemServicePrice, ClotheCategory, LaundryService, LaundryTranInfor, FBType, FBMeal, FBTranInfor

from booking.models import RentalInfor
from store.models import Room

from datetime import datetime

from basket.basket import LaudryBasket, FBMealBasket

def fb_meal_all(request):
    fb_types = FBType.objects.all()
    fb_meals = FBMeal.objects.all()

    return render(request, 'service/fb-meal-all.html', {'fb_types':fb_types, 'fb_meals':fb_meals})

def fb_meal_summary(request):
    fb_basket_obj = FBMealBasket(request)
    fb_basket = FBMealBasket(request).fb_basket.values()
    cost_before_tax = fb_basket_obj.get_cost_before_tax()
    total_tax = fb_basket_obj.get_total_tax()
    total_cost_with_tax = fb_basket_obj.get_total_cost_with_tax()
    return render(request, 'service/fb-summary.html', {'fb_basket':fb_basket, 'cost_before_tax':cost_before_tax, 'total_tax':total_tax, 'total_cost_with_tax':total_cost_with_tax})

# laundry
def food_drink_store(request):
    laundry_items = LaundryItemServicePrice.objects.all()
    clothe_types = ClotheCategory.objects.all()
    laundry_services = LaundryService.objects.all()
    return render(request, 'service/food-drink-sell.html', {'laundry_items':laundry_items, 'clothe_types':clothe_types, 'laundry_services':laundry_services})

# laundry
def food_drink_summary(request):
    laundry_basket_obj = LaudryBasket(request)
    laundry_basket = LaudryBasket(request).laundry_basket.values()
    cost_before_tax = laundry_basket_obj.get_cost_before_tax()
    total_tax = laundry_basket_obj.get_total_tax()
    total_cost_with_tax = laundry_basket_obj.get_total_cost_with_tax()

    return render(request, 'service/food-drink-summary.html', {'laundry_basket':laundry_basket, 'cost_before_tax':cost_before_tax, 'total_tax':total_tax, 'total_cost_with_tax':total_cost_with_tax})

def update_laundry_tran_db(request):
    laundry_basket = LaudryBasket(request)
    if request.POST.get('action') == 'post':
        roomCode = request.POST.get('roomName')
    
    # today_date = datetime.now()
    # today_date_str = today_date.strftime("%Y-%m-%d")

    today_str = str(datetime.now().date())
    today = datetime.strptime(today_str, "%Y-%m-%d")

    # 108.90 rent amount total LotusB02
    # roomCode = 'LotusB02'

    room_obj = Room.rooms.get(room_code=roomCode)

    rental_tran_objs = RentalInfor.objects.filter(room_id=room_obj, rental_date=today)
    rental_tran_obj = rental_tran_objs.first()
    total_cost = rental_tran_obj.rent_amount_total

    cost_before_tax = laundry_basket.get_cost_before_tax()
    tax = laundry_basket.get_total_tax()
    cost_with_tax = laundry_basket.get_total_cost_with_tax()

    laundry_tran_row = LaundryTranInfor.objects.create(
        rental_id = rental_tran_obj,
        room_id = room_obj,
        amount_paid = cost_before_tax,
        amount_tax = tax,
        total_amount_paid = cost_with_tax
    )
    response = JsonResponse({'name': "Pham Van Thai"})
    request.session['laundry'].clear()
    request.session.modified = True
    return response

def update_fb_tran_db(request):
    fb_basket = FBMealBasket(request)

    if request.POST.get('action') == 'post':
        roomCode = request.POST.get('roomName')

    # roomCode = 'LotusB02'

    today_str = str(datetime.now().date())
    today = datetime.strptime(today_str, "%Y-%m-%d")

    room_obj = Room.rooms.get(room_code=roomCode)
    rental_tran_objs = RentalInfor.objects.filter(room_id=room_obj, rental_date=today)
    rental_tran_obj = rental_tran_objs.first()

    cost_before_tax = fb_basket.get_cost_before_tax()
    tax = fb_basket.get_total_tax()
    cost_with_tax = fb_basket.get_total_cost_with_tax()

    fb_tran_row = FBTranInfor.objects.create(
        rental_id = rental_tran_obj,
        room_id = room_obj,
        amount_paid = cost_before_tax,
        amount_tax = tax,
        total_amount_paid = cost_with_tax
    )

    response = JsonResponse({'name': "Pham Van Thai"})
    request.session['fb_meal'].clear()
    request.session.modified = True
    return response