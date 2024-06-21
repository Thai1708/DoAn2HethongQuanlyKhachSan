from decimal import Decimal
from django.shortcuts import get_object_or_404

from store.models import Room, RoomType
from service.models import MealCode

# class BookingData():
#     """
#     A base Basket class, providing some default behaviors that
#     can be inherited or overrided, as necessary.
#     """

#     def __init__(self, request):
#         self.session = request.session
#         booking_data = self.session.get('booking_data')
#         if 'booking_data' not in request.session:
#             booking_data = self.session['booking_data'] = {}
#         self.booking_data = booking_data

#     def add(self, checkin_date_str, checkout_date_str):
#         if 'checkin_date' in self.booking_data and 'checkout_date' in self.booking_data:
#             self.booking_data['checkin_date'] = checkin_date_str
#             self.booking_data['checkout_date'] = checkout_date_str
#         else:
#             self.booking_data = {'checkin_date':checkin_date_str, 'checkout_date':checkout_date_str}
        
#         self.save()

#     def save(self):
#         self.session.modified = True
#         self.session.save()  # Thêm dòng này để chắc chắn session được lưu

class FBMealBasket():
    """
    A base Basket class, providing some default behaviors that
    can be inherited or overrided, as necessary.
    """

    def __init__(self, request):
        self.session = request.session
        fb_basket = self.session.get('fb_meal')
        if 'fb_meal' not in request.session:
            fb_basket = self.session['fb_meal'] = {}
        self.fb_basket = fb_basket   
    
    def add(self, fb_item, fb_item_name, itemqty, price, fb_item_image_url):
        """
        Adding and updating the users basket session data
        """
        fb_item_id = str(fb_item.id)

        total_cost_each = itemqty * price

        if fb_item_id in self.fb_basket:
            self.fb_basket[fb_item_id]['item_name'] = fb_item_name
            self.fb_basket[fb_item_id]['itemqty'] = itemqty
            self.fb_basket[fb_item_id]['price'] = price
            self.fb_basket[fb_item_id]['total_cost_each'] = total_cost_each
            self.fb_basket[fb_item_id]['fb_item_image_url'] = fb_item_image_url
        else:
            self.fb_basket[fb_item_id] = {'item_name':fb_item_name, 'itemqty': itemqty, 'price': price, 'total_cost_each': total_cost_each, 'laundry_item_image_url':fb_item_image_url}

        self.save()

    def get_cost_before_tax(self):
        return sum(item['total_cost_each'] for item in self.fb_basket.values())
    
    def get_total_tax(self):
        return round(sum(item['total_cost_each']/10 for item in self.fb_basket.values()), 2)
    
    def get_total_cost_with_tax(self):
        total_cost_with_tax = round(sum(item['total_cost_each']*1.1 for item in self.fb_basket.values()), 1)
        return total_cost_with_tax
    
    def save(self):
        self.session.modified = True

class LaudryBasket():
    """
    A base Basket class, providing some default behaviors that
    can be inherited or overrided, as necessary.
    """

    def __init__(self, request):
        self.session = request.session
        laundry_basket = self.session.get('laundry')
        if 'laundry' not in request.session:
            laundry_basket = self.session['laundry'] = {}
        self.laundry_basket = laundry_basket

    def add(self, laundry_item, laundry_item_name, itemqty, price, laundry_item_image_url):
        """
        Adding and updating the users basket session data
        """
        laundry_item_id = str(laundry_item.id)

        total_cost_each = itemqty * price

        if laundry_item_id in self.laundry_basket:
            self.laundry_basket[laundry_item_id]['item_name'] = laundry_item_name
            self.laundry_basket[laundry_item_id]['itemqty'] = itemqty
            self.laundry_basket[laundry_item_id]['price'] = price
            self.laundry_basket[laundry_item_id]['total_cost_each'] = total_cost_each
            self.laundry_basket[laundry_item_id]['laundry_item_image_url'] = laundry_item_image_url
        else:
            self.laundry_basket[laundry_item_id] = {'item_name':laundry_item_name, 'itemqty': itemqty, 'price': price, 'total_cost_each': total_cost_each, 'laundry_item_image_url':laundry_item_image_url}

        self.save()

    def get_cost_before_tax(self):
        return sum(item['total_cost_each'] for item in self.laundry_basket.values())
    
    def get_total_tax(self):
        return sum(item['total_cost_each']/10 for item in self.laundry_basket.values())
    
    def get_total_cost_with_tax(self):
        total_cost_with_tax = round(sum(item['total_cost_each']*1.1 for item in self.laundry_basket.values()), 1)
        return total_cost_with_tax

    def save(self):
        self.session.modified = True



    # def update(self, product, qty):
    #     """
    #     Update values in session data
    #     """
    #     product_id = str(product)
    #     if product_id in self.basket:
    #         self.basket[product_id]['qty'] = qty
    #     self.save()

class Basket():
    """
    A base Basket class, providing some default behaviors that
    can be inherited or overrided, as necessary.
    """

    def __init__(self, request):
        self.session = request.session
        basket = self.session.get('skey')
        if 'skey' not in request.session:
            basket = self.session['skey'] = {}
        self.basket = basket

    def add(self, room, qty, adult_qty, child_qty, meal_code):
        """
        Adding and updating the users basket session data
        """
        room_id = str(room.id)

        if room_id in self.basket:
            self.basket[room_id]['qty'] = qty
            self.basket[room_id]['adult_qty'] = adult_qty
            self.basket[room_id]['child_qty'] = child_qty
            self.basket[room_id]['meal_code'] = meal_code
        else:
            self.basket[room_id] = {'price': str(room.price), 'qty': qty, 'adult_qty': adult_qty, 'child_qty':child_qty, 'meal_code':meal_code}

        self.save()

    def __iter__(self):
        """
        Collect the product_id in the session data to query the database
        and return products
        """
        room_ids = self.basket.keys()
        room_id_list = list(room_ids)
        basket = self.basket.copy()
        rooms = Room.rooms.filter(id__in=room_ids)
        for room in rooms:
            basket[str(room.id)]['room'] = room
        
        meal_codes = []
        for value in self.basket.values():
            meal_codes.append(value['meal_code'])

      
        for i in range(len(room_id_list)):
            meal_code_object = MealCode.objects.filter(meal_code=meal_codes[i]).first()  # Sử dụng first() để lấy đối tượng đầu tiên trong QuerySet
            if meal_code_object:
                basket[str(room_id_list[i])]['meal_code_obj'] = meal_code_object
            else:
                # Tạo một đối tượng MealCode mới với adult_price và child_price bằng 0
                meal_code_dummy = MealCode(adult_price=0, child_price=0)
                basket[str(room_id_list[i])]['meal_code_obj'] = meal_code_dummy

        for item in basket.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['qty']
            item['adult_meal_cost'] = item['meal_code_obj'].adult_price * item['adult_qty'] *90/100
            item['child_meal_cost'] = item['meal_code_obj'].child_price * item['child_qty'] *90/100 # Đăng ký qua website được giảm 10 phần trăm
            yield item

    def __len__(self):
        """
        Get the basket data and count the qty of items
        """
        return sum(item['qty'] for item in self.basket.values())

    def get_total_meal_cost(self):
        return sum(Decimal(item['adult_meal_cost']) + Decimal(item['child_meal_cost']) for item in self) # Sử dụng iter để lặp

    # công thức tính tiền phòng
    def get_cost_before_tax(self):
        return sum(Decimal(item['price']) * item['qty'] for item in self)
    
    # công thức tính tổng số tiền
    def get_total_cost_before_tax(self):
        return sum((Decimal(item['price']) * item['qty'] + Decimal(item['adult_meal_cost']) + Decimal(item['child_meal_cost'])) for item in self)

    # công thức tính số tiền thuế    
    def get_total_tax(self):
        return sum(((Decimal(item['price']) * item['qty'] + Decimal(item['adult_meal_cost']) + Decimal(item['child_meal_cost']))/10) for item in self)

    # công thức tính tổng số tiền cần thanh toán bao gồm thuế
    def get_total_cost_with_tax(self):
        return sum((Decimal(item['price']) * item['qty'] + Decimal(item['adult_meal_cost']) + Decimal(item['child_meal_cost']))*110/100 for item in self)
    
    # tính số người sẽ ở khách sạn
    def get_adult_qty(self):
        return sum(item['adult_qty'] for item in self)
    
    def get_child_qty(self):
        return sum(item['child_qty'] for item in self)

    def delete(self, room):
        """
        Delete item from session data
        """
        room_id = str(room)

        if room_id in self.basket:
            del self.basket[room_id]
            print(room_id)
            self.save()

    def save(self):
        self.session.modified = True

    # def update(self, product, qty):
    #     """
    #     Update values in session data
    #     """
    #     product_id = str(product)
    #     if product_id in self.basket:
    #         self.basket[product_id]['qty'] = qty
    #     self.save()
