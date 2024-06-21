from django.shortcuts import render
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.http import JsonResponse
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers import serialize
import json
# from django.utils.decorators import method_decorator


from .handle_decimal import DecimalEncoder

from .models import BookingInfor, TranInfor, Country, RentalInfor, PaymentMethod, Promo, PaymentTranInfor
from basket.basket import Basket
from human_resource.models import Guest
from store.models import Room, RoomType
from service.models import MealCode, MealChargeTranInfor, FBTranInfor, LaundryTranInfor

from datetime import datetime, timedelta
from decimal import Decimal

def booking_invoice(request, pk):
    today_str = str(datetime.now().date())
    booking_infor = get_object_or_404(BookingInfor, id=pk)
    
    tran_infors = TranInfor.objects.filter(booking_id= booking_infor)
    rental_infors = RentalInfor.objects.filter(tran_id__in=tran_infors)
    # tiền ăn uống tại khách sạn
    fb_trans = FBTranInfor.objects.filter(rental_id__in=rental_infors)
    try:
        total_meal_cost = fb_trans.aggregate(total_cost=Sum('total_amount_paid'))['fb_total_cost']
    except:
        total_meal_cost = 0

    # giặt là
    laundry_trans = LaundryTranInfor.objects.filter(rental_id__in=rental_infors)
    try:
        total_laudry_cost = laundry_trans.aggregate(total_cost=Sum('total_amount_paid'))['total_laudry_cost']
    except:
        total_laudry_cost = 0

    # tiền phòng và dịch vụ đặt qua website đã có khuyến mãi
    payment_for_total = round(float(booking_infor.payment_for_total), 2)
    print("####################")
    print(total_meal_cost)
    print(total_laudry_cost)
    print(payment_for_total)
    print("####################")
    # tien dat coc
    payment_deposit = round(payment_for_total/2, 2)
    # tong so tien cuoi cung
    payment_final = round(payment_for_total + total_laudry_cost + total_meal_cost, 2)
    # thue
    tax = round(payment_final/11, 2)
    # so tien con phai tra
    payment_remain = payment_final - payment_deposit


    return render(request, 'checkout/booking_invoice.html', {'booking_infor':booking_infor, 'today_str':today_str, 'payment_for_total':payment_for_total, 'total_meal_cost':total_meal_cost, 'total_laudry_cost':total_laudry_cost, 'payment_deposit':payment_deposit, 'tax':tax, 'payment_final':payment_final, 'payment_remain':payment_remain})

def checkout_page(request):
    today_str = str(datetime.now().date())
    today = datetime.strptime(today_str, "%Y-%m-%d")

    booking_infors = BookingInfor.objects.filter(departure_date=today)
    # tran_infors = TranInfor.objects.filter(booking_id__in =booking_infors)
    # tran_infors = TranInfor.objects.all()
    # tran_infor = TranInfor()
    return render(request, 'checkout/checkout.html', {'booking_infors':booking_infors, 'today_str':today_str})

def save_promo_to_session(request):
    if request.POST.get('action') == 'post':
        total_for_payment = request.POST.get('value')
    request.session['total_for_payment'] = total_for_payment
    response = JsonResponse({'name': 'Phạm Văn Thái'});
    return response

def visa_payment(request):
    total_for_payment = request.session['total_for_payment']
    if 'checkin' in request.session and 'checkout' in request.session:
        arrival_date_str = request.session['checkin']
        departure_date_str = request.session['checkout']
        arrival_date = datetime.strptime(arrival_date_str, "%Y-%m-%d")
        departure_date = datetime.strptime(departure_date_str, "%Y-%m-%d")
        days_difference = int((departure_date - arrival_date).days)
        total_for_payment_entire_trip = round(float(total_for_payment)*days_difference, 2)
    else:
        total_for_payment_entire_trip = total_for_payment
    countries = Country.objects.all()
    payments = PaymentMethod.objects.all()
    
    return render(request, 'payment/visa_payment.html', {'countries':countries, 'payments':payments, 'total_for_payment':total_for_payment, 'total_for_payment_entire_trip':total_for_payment_entire_trip, 'arrival_date_str':arrival_date_str, 'departure_date_str':departure_date_str})

def search_booking_room(request):
    # booking_data = BookingData(request)
    if request.POST.get('action') == 'post':
        checkin_date_str = str(request.POST.get('checkin_date'))
        checkout_date_str = str(request.POST.get('checkout_date'))
        adultqty_search = str(request.POST.get('adultqty_search'))
        roomtype_search = str(request.POST.get('roomtype_search'))
        print(checkin_date_str, checkout_date_str)

        request.session['checkin'] = checkin_date_str
        request.session['checkout'] = checkout_date_str

        request.session.modified = True
    print(request.session['checkin'])
    print(request.session['checkout'])

        # booking_data.add(checkin_date_str=checkin_date_str, checkout_date_str=checkout_date_str)
        # print(booking_data.booking_data)

     # convert string dates to date objects
    checkin_date = datetime.strptime(checkin_date_str, '%Y-%m-%d')
    checkout_date = datetime.strptime(checkout_date_str, '%Y-%m-%d')
    print(checkin_date, checkout_date)
    print(adultqty_search, roomtype_search)



    # query for RentalInfor in the specified date range
    rentals = RentalInfor.objects.filter(
        rental_date__range=(checkin_date, checkout_date)
    )

    # Xây dựng Q objects cho các điều kiện tìm kiếm
    if roomtype_search == 'Loại phòng':
        roomtype_search = ''
    # if adultqty_search == 'Số người mỗi phòng':
    #     adultqty_search = ''    
    conditions = Q()

    if roomtype_search:
        conditions &= Q(name=roomtype_search)

    # if adultqty_search:
    #     conditions &= Q(bed_adult=adultqty_search)

    # Lấy room_types với các điều kiện đã xây dựng
    room_types = RoomType.objects.filter(conditions)

    # extract room_ids
    room_ids = rentals.values_list('room_id', flat=True).distinct()

    # optionally, get room objects if needed
    rooms_query_sub = Room.rooms.exclude(id__in=room_ids, room_type_id__in=room_types)
    rooms_query = rooms_query_sub.filter(room_type_id__in=room_types)

    # 

    # Render the bookings to an HTML template
    rendered_template = render(request, 'room/room_all_search.html', {'rooms_query': rooms_query}).content.decode('utf-8')

    # # Return the rendered HTML as part of the JSON response
    response = JsonResponse({'html': rendered_template})
    return response

def update_booking_db(request):
    basket = Basket(request)
    
    # lấy thông tin từ form thanh toán
    if request.POST.get('action') == 'post':
        firstName = request.POST.get('firstName')
        lastName = request.POST.get('lastName')
        email = request.POST.get('email')
        address = request.POST.get('address')
        phonenumber = request.POST.get('phonenumber')
        country = request.POST.get('country')
        # state = int(request.POST.get('state'))
        zipcode = request.POST.get('zip')
        paymentMethod = request.POST.get('paymentMethod')
        totalForPaymentPerDay = request.POST.get('totalForPayment')
        # cardName = int(request.POST.get('cardName'))
        # cardNumber = int(request.POST.get('cardNumber'))

    # lấy thông tin từ basket    

    guest = Guest.objects.create(
                first_name=firstName,
                last_name=lastName,
            )
    
    # arrival_date_str = '2024-06-06'
    arrival_date_str = request.session['checkin']
    arrival_date = datetime.strptime(arrival_date_str, "%Y-%m-%d")

    # departure_date_str = '2024-06-07'
    departure_date_str = request.session['checkout']
    departure_date = datetime.strptime(departure_date_str, "%Y-%m-%d")
    # tính số ngày giữa hai ngày
    days_difference = int((departure_date - arrival_date).days)
    # so tien can thanh toan trong n ngay
    totalForPayment = float(totalForPaymentPerDay)*days_difference

    print(arrival_date_str, departure_date_str, days_difference, totalForPayment)

    # Tạo danh sách các ngày
    date_list = []
    current_date = arrival_date
    while current_date < departure_date:
        date_list.append(current_date)
        current_date += timedelta(days=1)
    
    country_obj = Country.objects.get(country_code=country)

    adult_qty = basket.get_adult_qty()
    child_qty = basket.get_child_qty()

    booking_infor = BookingInfor.objects.create(
        first_name = firstName,
        last_name = lastName,
        email = email,
        phone_number = phonenumber,
        address = address,
        zipcode = zipcode,
        country_link = country_obj,
        arrival_date = arrival_date,
        departure_date = departure_date,
        adults = adult_qty,
        childs = child_qty,
        nights = days_difference,
        guest_id = guest,
        payment_for_total = totalForPayment
    )

    # payment_method = PaymentMethod.objects.get(name=paymentMethod)

    payment_infor = PaymentTranInfor.objects.create(
        booking_infor = booking_infor,
        payment_method = paymentMethod,
        amount_paid = totalForPayment,
        current_amount_paid = totalForPayment
    )

    for key, value in basket.basket.items():
        room_id = str(key)
        adult_qty_each_room = value['adult_qty']
        child_qty_each_room = value['child_qty']

        # thiếu nhân với số nights, nights được tính bằng phép trừ ngày departure cho arrival
        # tạm thời tran_infor sẽ sử dụng total_rent_each_day chưa đúng, total_rent_each_tran mới đúng
        total_rent_each_day = int(value['price'])
        total_rent_tax_each_day = int(value['price'])/10
        total_rent_overall_each_day = float(total_rent_each_day + total_rent_tax_each_day)

        total_rent = int(value['price']) * days_difference
        total_rent_tax = int(value['price'])/10 * days_difference
        total_rent_overall = float(total_rent + total_rent_tax) * days_difference


        meal_code = value['meal_code']
        meal_obj = MealCode.objects.get(meal_code=meal_code)
        adult_meal_cost = int(adult_qty_each_room)*meal_obj.adult_price*days_difference
        child_meal_cost = int(child_qty_each_room)*meal_obj.child_price*days_difference
        meal_cost = float(adult_meal_cost + child_meal_cost)*0.9 # đặt qua web giảm 10 phần trăm
        meal_cost_tax = meal_cost/10

        adult_meal_cost_per_day = int(adult_qty_each_room)*meal_obj.adult_price
        child_meal_cost_per_day = int(child_qty_each_room)*meal_obj.child_price
        meal_cost_per_day = float(adult_meal_cost + child_meal_cost)*0.9 # đặt qua web giảm 10 phần trăm
        meal_cost_tax_per_day = meal_cost_per_day/10
        meal_cost_total_per_day = round((meal_cost_per_day+meal_cost_tax_per_day),2)

        deposit = (total_rent + total_rent_tax + meal_cost + meal_cost_tax)/2
        total_amount_paid = (total_rent + total_rent_tax + meal_cost + meal_cost_tax)


        room_obj = Room.rooms.get(id=room_id)
        tran_infor = TranInfor.objects.create(
            booking_id = booking_infor,
            room_id = room_obj,
            adults = adult_qty_each_room,
            childs = child_qty_each_room,
            total_rent = total_rent,
            total_rent_tax = total_rent_tax,
            total_deposit = deposit,
            total_other_charges = meal_cost,
            total_other_charges_tax = meal_cost_tax,
            total_amount_paid = total_amount_paid
        )

        for date in date_list:
            rental_infor = RentalInfor.objects.create(
                tran_id = tran_infor,
                room_id = room_obj,
                rental_date = date,
                rent_amount = total_rent_each_day,
                rent_amount_tax = total_rent_tax_each_day,
                rent_amount_total = total_rent_overall_each_day,
                meal_cost = meal_cost_per_day,
                meal_cost_tax = meal_cost_tax_per_day,
                meal_cost_total = meal_cost_total_per_day
            )

    response = JsonResponse({'name': "Pham Van Thai"});
    basket.basket.clear()
    basket.session.modified = True
    # return redirect(reverse('store:room_all'))
    return response

@csrf_exempt
def calculate_promo(request):
    basket = Basket(request)
    if request.method == 'POST':
        promo_code = str(request.POST.get('fname'))

    try:
        promo_obj = Promo.objects.get(promo_code=promo_code)
        discount = promo_obj.discount
        total_for_payment = basket.get_total_cost_with_tax()*(100-discount)/100
        
    except Promo.DoesNotExist:
        total_for_payment = basket.get_total_cost_with_tax()

    response = JsonResponse({'total_for_payment': str(total_for_payment)});
    return response