from django.db import models
from django.urls import reverse

from booking.models import TranInfor, RentalInfor, Charges
from human_resource.models import Guest
from store.models import Room

class MealCode(models.Model):
    meal_code = models.CharField(max_length=50)
    image = models.ImageField(upload_to='images/', default='images/default.png')
    description = models.CharField(max_length=250)
    adult_price = models.DecimalField(max_digits=15,decimal_places=2, default=0)
    child_price = models.DecimalField(max_digits=15,decimal_places=2, default=0)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=255, default='front-desk')
    modified_by = models.CharField(max_length=255, default='front-desk')
    is_deleted = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Meals'
        ordering = ('-created_date',)

    def __str__(self):
        return self.meal_code

class MealChargeTranInfor(models.Model):
    tran_infor = models.ForeignKey(TranInfor, on_delete=models.CASCADE)
    rental_infor = models.ForeignKey(RentalInfor, on_delete=models.CASCADE)
    meal_code = models.ForeignKey(MealCode, on_delete=models.SET_NULL, null=True)
    quantity_adult = models.IntegerField(default=1)
    quantity_child = models.IntegerField(default=1)
    is_booked_before = models.BooleanField(default=False) # Meal plan da duoc dat tu truoc hay chua
    charge = models.ForeignKey(Charges, on_delete=models.SET_NULL, null=True)
    # guest = models.ForeignKey(Guest, on_delete=models.SET_NULL, null=True)
    # is_adult = models.BooleanField(default=True)

    amount_paid = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    rent_tax = models.DecimalField(max_digits=15,decimal_places=2, default=0)
    rent_total = models.DecimalField(max_digits=15,decimal_places=2, default=0)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=255, default='front-desk')
    modified_by = models.CharField(max_length=255, default='front-desk')
    is_deleted = models.BooleanField(default=False)

class LaundryService(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=255, default='front-desk')
    modified_by = models.CharField(max_length=255, default='front-desk')
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class ClotheCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=255, default='front-desk')
    modified_by = models.CharField(max_length=255, default='front-desk')
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class LaundryItemServicePrice(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/', default='images/default.png')
    # slug = models.SlugField(max_length=255)
    description = models.CharField(max_length=255)
    laundry_service_id = models.ForeignKey(LaundryService, on_delete=models.SET_NULL, null=True)
    clothe_category_id = models.ForeignKey(ClotheCategory, on_delete=models.SET_NULL, null=True)
    cost = models.FloatField()

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=255, default='front-desk')
    modified_by = models.CharField(max_length=255, default='front-desk')
    is_deleted = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'LaundryItemServicePrices'
        ordering = ('-created_date',)
    
    def __str__(self):
        return self.name
    
class LaundryExtraService(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    cost = models.FloatField()

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=255, default='front-desk')
    modified_by = models.CharField(max_length=255, default='front-desk')
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
class LaundryTranInfor(models.Model):
    # link voi tran va rental co day du thong tin cua khach roi
    # tran_id = models.ForeignKey(TranInfor, on_delete=models.CASCADE, null=True, blank=True)
    rental_id = models.ForeignKey(RentalInfor, on_delete=models.CASCADE)
    room_id = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True)
    # khong can thiet lam, do don vi tinh bao gom ca kg va cai
    total_items = models.IntegerField(blank=True, null=True)
    laundry_extra_service_id = models.ForeignKey(LaundryExtraService, blank=True, null=True, on_delete=models.SET_NULL)
    amount_paid = models.FloatField()
    amount_tax = models.FloatField()
    total_amount_paid = models.FloatField()
    guest_laundry_time = models.DateTimeField(blank=True, null=True)
    delivery_time = models.DateTimeField(blank=True, null=True)
    description = models.CharField(max_length=255)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=255, default='front-desk')
    modified_by = models.CharField(max_length=255, default='front-desk')
    is_deleted = models.BooleanField(default=False)

    # def __str__(self):
    #     return self.name

class FBType(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=255, default='admin')
    modified_by = models.CharField(max_length=255, default='admin')
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
class FBMeal(models.Model):
    name = models.CharField(max_length=255)
    fb_type = models.ForeignKey(FBType, models.CASCADE)
    description = models.CharField(max_length=255)
    cost = models.FloatField()
    image = models.ImageField(upload_to='images/', default='images/default.png')

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=255, default='admin')
    modified_by = models.CharField(max_length=255, default='admin')
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class FBTranInfor(models.Model):
    # link voi tran va rental co day du thong tin cua khach roi
    # tran_id = models.ForeignKey(TranInfor, on_delete=models.CASCADE, null=True, blank=True)
    rental_id = models.ForeignKey(RentalInfor, on_delete=models.CASCADE)
    room_id = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True)
    # khong can thiet lam, do don vi tinh bao gom ca kg va cai
    amount_paid = models.FloatField()
    amount_tax = models.FloatField()
    total_amount_paid = models.FloatField()
    transaction_time = models.DateTimeField(auto_now=True)
    description = models.CharField(max_length=255)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=255, default='front-desk')
    modified_by = models.CharField(max_length=255, default='front-desk')
    is_deleted = models.BooleanField(default=False)

    # def __str__(self):
    #     return self.name
