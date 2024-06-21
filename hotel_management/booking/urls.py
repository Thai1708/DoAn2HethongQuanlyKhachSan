from django.urls import path

from . import views

app_name = 'booking'

urlpatterns = [
    path('visa_payment/', views.visa_payment, name='visa_payment'),
    path('search_booking_room/', views.search_booking_room, name='search_booking_room'),
    path('update_booking_db/', views.update_booking_db, name='update_booking_db'),
    path('calculate_promo/', views.calculate_promo, name='calculate_promo'),
    path('save_promo_to_session/', views.save_promo_to_session, name='save_promo_to_session'),
    path('checkout_page/', views.checkout_page, name='checkout_page'),
    path('booking_invoice/<str:pk>/', views.booking_invoice, name='booking_invoice'),
    
]