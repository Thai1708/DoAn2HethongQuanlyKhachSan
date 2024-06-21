from django.shortcuts import render

from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render

from store.models import Room, RoomType

from .basket import Basket, LaudryBasket, FBMealBasket

from service.models import LaundryItemServicePrice, FBMeal


def reservation_detail(request):
    basket = Basket(request)
    return render(request, 'reservation_detail.html', {'basket': basket})


def basket_add(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        room_id = int(request.POST.get('roomid'))
        room_qty = int(request.POST.get('roomqty'))
        meal_code = request.POST.get('mealcode')
        adul_tqty = int(request.POST.get('adultqty'))
        child_qty = int(request.POST.get('childqty'))
        room = get_object_or_404(Room, id=room_id)
        basket.add(room=room, qty=room_qty, adult_qty=adul_tqty, child_qty=child_qty, meal_code=meal_code)

        basketqty = basket.__len__()
        response = JsonResponse({'qty': basketqty})
        return response

def basket_delete(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        room_id = int(request.POST.get('roomid'))
        basket.delete(room=room_id)

        basketqty = basket.__len__()
        baskettotal = basket.get_cost_before_tax()
        response = JsonResponse({'qty': basketqty, 'subtotal': baskettotal})
        return response

def laundry_basket_add(request):
    laundry_basket = LaudryBasket(request)
    if request.POST.get('action') == 'post':
        laundry_item_id = int(request.POST.get('laundryItemID'))
        itemqty = int(request.POST.get('itemqty'))
        price = float(request.POST.get('price'))
        laundry_item = get_object_or_404(LaundryItemServicePrice, id=laundry_item_id)
        laundry_item_image_url = laundry_item.image.url
        laundry_item_name = laundry_item.name
        laundry_basket.add(laundry_item=laundry_item, laundry_item_name=laundry_item_name, itemqty=itemqty, price=price, laundry_item_image_url=laundry_item_image_url)

    print(laundry_item_id, itemqty, price)
    response = JsonResponse({'name': 'Phạm Văn Thái'});
    return response
    
def fb_meal_basket_add(request):
    fb_basket = FBMealBasket(request)
    if request.POST.get('action') == 'post':
        fb_item_id = int(request.POST.get('fbItemID'))
        itemqty = int(request.POST.get('itemqty'))
        price = float(request.POST.get('price'))
        fb_item = get_object_or_404(FBMeal, id=fb_item_id)
        fb_item_image_url = fb_item.image.url
        fb_item_name = fb_item.name
        fb_basket.add(fb_item=fb_item, fb_item_name=fb_item_name, itemqty=itemqty, price=price, fb_item_image_url=fb_item_image_url)

    response = JsonResponse({'name': 'Phạm Văn Thái'});
    return response


# def basket_update(request):
#     basket = Basket(request)
#     if request.POST.get('action') == 'post':
#         product_id = int(request.POST.get('productid'))
#         product_qty = int(request.POST.get('productqty'))
#         basket.update(product=product_id, qty=product_qty)

#         basketqty = basket.__len__()
#         baskettotal = basket.get_total_price()
#         response = JsonResponse({'qty': basketqty, 'subtotal': baskettotal})
#         return response
