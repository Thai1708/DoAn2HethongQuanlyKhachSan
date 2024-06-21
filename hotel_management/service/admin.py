from django.contrib import admin

from .models import MealCode, MealChargeTranInfor, LaundryService, ClotheCategory, LaundryItemServicePrice, LaundryTranInfor, LaundryExtraService, FBMeal, FBType, FBTranInfor

admin.site.register(MealChargeTranInfor)
admin.site.register(MealCode)
admin.site.register(LaundryService)
admin.site.register(ClotheCategory)
admin.site.register(LaundryItemServicePrice)
admin.site.register(LaundryTranInfor)
admin.site.register(LaundryExtraService)
admin.site.register(FBMeal)
admin.site.register(FBType)
admin.site.register(FBTranInfor)


