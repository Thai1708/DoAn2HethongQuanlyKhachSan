from django.urls import path

from . import views

app_name = 'basket'

urlpatterns = [
    path('', views.reservation_detail, name='reservation_detail'),
    path('add/', views.basket_add, name='basket_add'),
    path('delete/', views.basket_delete, name='basket_delete'),
    path('laundry_basket_add/', views.laundry_basket_add, name='laundry_basket_add'),
    path('fb_meal_basket_add/', views.fb_meal_basket_add, name='fb_meal_basket_add'),
    # path('delete/', views.basket_delete, name='basket_delete'),
    # path('update/', views.basket_update, name='basket_update'),
]