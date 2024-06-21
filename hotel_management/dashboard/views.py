from django.shortcuts import render
from datetime import datetime, timedelta
from django.db.models import Sum

from booking.models import RentalInfor, BookingInfor
from store.models import Room
from service.models import FBTranInfor

def daily_report(request):
    today_str = str(datetime.now().date())
    today = datetime.strptime(today_str, "%Y-%m-%d")

    # tinh so phong
    rental_infors = RentalInfor.objects.filter(rental_date=today)
    booking_infors = BookingInfor.objects.filter(arrival_date__lte=today, departure_date__gte=today)
    total_adults = booking_infors.aggregate(total_adults=Sum('adults'))['total_adults']
    total_childs = booking_infors.aggregate(total_childs=Sum('childs'))['total_childs']
    total_guests = int(total_adults) + int(total_childs)

    room_revenue = rental_infors.aggregate(room_revenue=Sum('rent_amount_total'))['room_revenue']
    meal_revenue = rental_infors.aggregate(meal_revenue=Sum('meal_cost_total'))['meal_revenue']
    # try:
    #     fb_revenue = FBTranInfor.objects.filter()

    revenue_daily = round(float(room_revenue)+float(meal_revenue), 2)

    occupied_rooms = rental_infors.count()
    total_rooms = Room.rooms.all().count()
    available_rooms = total_rooms - occupied_rooms

    # Doanh thu theo loai phong
    # single_room_retals = rental_infors.filter()

    return render(request, 'dashboard/daily_report.html', {'occupied_rooms':occupied_rooms, 'available_rooms':available_rooms, 'total_guests':total_guests, 'revenue_daily':revenue_daily, 'today_str':today_str})
