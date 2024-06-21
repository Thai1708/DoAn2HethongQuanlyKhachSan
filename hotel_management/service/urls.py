from django.urls import path

from . import views

app_name = 'service'

urlpatterns = [
    path('food_drink_store/', views.food_drink_store, name='food_drink_store'),
    path('food_drink_summary/', views.food_drink_summary, name='food_drink_summary'),
    path('update_laundry_tran_db/', views.update_laundry_tran_db, name='update_laundry_tran_db'),
    path('fb_meal_all/', views.fb_meal_all, name='fb_meal_all'),
    path('fb_meal_summary/', views.fb_meal_summary, name='fb_meal_summary'),
    path('update_fb_tran_db/', views.update_fb_tran_db, name='update_fb_tran_db'),
    
]