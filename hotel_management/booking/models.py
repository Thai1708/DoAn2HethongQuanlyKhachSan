from django.urls import reverse
from django.db import models

from human_resource.models import User

from human_resource.models import Employee, Guest
from store.models import Room

class Country(models.Model):
    country_code = models.CharField(max_length=255)
    country_name = models.CharField(max_length=255)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=255, default='admin')
    modified_by = models.CharField(max_length=255, default='admin')
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.country_code

class BookingSource(models.Model):
    code = models.CharField(max_length=100)
    description = models.CharField(max_length=255)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=255, default='admin')
    modified_by = models.CharField(max_length=255, default='admin')
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.code

class HousekeepingStatus(models.Model):
    code = models.CharField(max_length=50)
    description = models.CharField(max_length=250)

    def __str__(self):
        return self.code

class AccountType(models.Model):
    code = models.CharField(max_length=50)
    description = models.CharField(max_length=250)

    def __str__(self):
        return self.code

class Charges(models.Model):
    code = models.CharField(max_length=50)
    account_type = models.ForeignKey(AccountType, on_delete=models.SET_NULL, null=True)
    description = models.CharField(max_length=250)

    def __str__(self):
        return self.code
    

class BookingInfor(models.Model):
    booking_date = models.DateTimeField(auto_now=True)
    booked_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='booking_employee', default=1) #User có id là 1
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, null=True)
    phone_number = models.CharField(max_length=30, null=True, blank=True)
    email = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    zipcode = models.CharField(max_length=50, null=True, blank=True)
    country_link = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    cancel_date = models.DateTimeField(null=True, blank=True) # Khi cancel date cho delete bằng True
    # is_canceled = models.BooleanField(default=False)
    arrival_date = models.DateTimeField()
    departure_date = models.DateTimeField()
    nights = models.IntegerField(default=0)
    adults = models.IntegerField(default=0)
    childs = models.IntegerField(default=0)

    # Thông tin liên quan đến nhân sự thực hiện booking đó.
    booking_source_id = models.ForeignKey(BookingSource, on_delete=models.SET_NULL, null=True, blank=True, default=1)
    saleman_id = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True, default=1) # Mặc định là lễ tân trưởng, sau đó lễ tân thực sự kiểm tra sẽ cập nhật lại.

    # Thông tin liên quan đến khách hàng.
    booking_user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='booking_user')
    is_cityledger = models.BooleanField(default=False)
    guest_id = models.ForeignKey(Guest, on_delete=models.SET_NULL, null=True, blank=True) # Nghiệp vụ, tạo 1 form, sau đó dùng dữ liệu của form đó, để cập nhật các bảng cơ sở dữ liệu. Do đó, cần thiết kế nhiều form.

    payment_for_total = models.FloatField(null=True, blank=True)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=255, default='front-desk')
    modified_by = models.CharField(max_length=255, default='front-desk')
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.first_name

class TranInfor(models.Model):
    # Được cập nhật bởi thông tin session/ cập nhật nhờ thông tin của Rental Infor, Service
    booking_id = models.ForeignKey(BookingInfor, on_delete=models.CASCADE, related_name='traninfor_set')
    room_id = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True)

    is_checked = models.BooleanField(default=False) # Lễ tân có trách nhiệm kiểm tra lại, ngay sau khi khách đặt và khi khách đến check in.
    checkin_date = models.DateTimeField(null=True,blank=True)
    checkout_date = models.DateTimeField(null=True, blank=True)
    cancel_date = models.DateTimeField(null=True, blank=True)
    adults = models.IntegerField(default=0)
    childs = models.IntegerField(default=0)

    total_rent = models.DecimalField(max_digits=15,decimal_places=2, default=0)
    total_rent_tax = models.DecimalField(max_digits=15,decimal_places=2, default=0)
    total_other_charges = models.DecimalField(max_digits=15,decimal_places=2, default=0) # CHi phi cho tat ca dich vu su dung
    total_other_charges_tax = models.DecimalField(max_digits=15,decimal_places=2, default=0)
    total_amount_paid = models.DecimalField(max_digits=15,decimal_places=2, default=0)
    total_deposit = models.DecimalField(max_digits=15,decimal_places=2, default=0)
    description = models.CharField(max_length=255, null=True)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=255, default='front-desk')
    modified_by = models.CharField(max_length=255, default='front-desk')
    is_deleted = models.BooleanField(default=False)

class RentalInfor(models.Model):
    tran_id = models.ForeignKey(TranInfor, on_delete=models.CASCADE)
    room_id = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True)
    charges = models.ForeignKey(Charges, on_delete=models.SET_NULL, null=True, default=1)
    rental_date = models.DateTimeField()
    rent_amount = models.DecimalField(max_digits=15,decimal_places=2, default=0)
    rent_amount_tax = models.DecimalField(max_digits=15,decimal_places=2, default=0)
    rent_amount_total = models.DecimalField(max_digits=15,decimal_places=2, default=0)
    # meal_code_id = models.ForeignKey(MealCode, on_delete=models.SET_NULL, null=True)
    meal_cost = models.DecimalField(max_digits=15,decimal_places=2, default=0)
    meal_cost_tax = models.DecimalField(max_digits=15,decimal_places=2, default=0)
    meal_cost_total = models.DecimalField(max_digits=15,decimal_places=2, default=0)
    old_hk_status = models.ForeignKey(HousekeepingStatus, on_delete=models.SET_NULL, null=True, related_name='old_hk_status')
    new_hk_status = models.ForeignKey(HousekeepingStatus, on_delete=models.SET_NULL, null=True, related_name='new_hk_status')

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=255, default='front-desk')
    modified_by = models.CharField(max_length=255, default='front-desk')
    is_deleted = models.BooleanField(default=False)

class PaymentMethod(models.Model):
    code = models.CharField(max_length=100)
    name = models.CharField(max_length=250)
    description = models.CharField(max_length=250, null=True)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=255, default='front-desk')
    modified_by = models.CharField(max_length=255, default='front-desk')
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.code

class PaymentTranInfor(models.Model):
    booking_infor = models.ForeignKey(BookingInfor, on_delete=models.SET_NULL, null=True)
    tran_date = models.DateTimeField(auto_now=True)
    # payment_method = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, null=True)
    payment_method = models.CharField(max_length=255, null=True, blank=True)
    amount_paid = models.DecimalField(max_digits=15,decimal_places=2, default=0)
    amount_debt = models.DecimalField(max_digits=15,decimal_places=2, default=0)
    current_amount_paid = models.DecimalField(max_digits=15,decimal_places=2, default=0)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=255, default='front-desk')
    modified_by = models.CharField(max_length=255, default='front-desk')
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.payment_method


class StayInfor(models.Model):
    tran_infor = models.ForeignKey(TranInfor, on_delete=models.CASCADE)
    guest = models.ForeignKey(Guest, on_delete=models.SET_NULL, null=True)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=255, default='front-desk')
    modified_by = models.CharField(max_length=255, default='front-desk')
    is_deleted = models.BooleanField(default=False)

class Promo(models.Model):
    # Mã này sẽ được tạo vào từng dịp, một cách thủ công.
    # Đặt tên theo cú pháp DISCOUNT-TÊN DỊP-THÁNG-NĂM
    promo_code = models.CharField(max_length=100)
    discount = models.IntegerField()
    description = models.CharField(max_length=255) # Phần description sẽ chứa ngày khả dụng cho mã.

    def __str__(self):
        return self.promo_code
