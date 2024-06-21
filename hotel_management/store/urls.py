from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('room_all/', views.room_all, name="room_all"),
    path('<slug:slug>', views.room_detail, name="room_detail"),

    # path('reservation_detail/', views.reservation_detail, name="reservation_detail"),
    path('service/', views.service, name="service"),
    path('service/service_meal', views.service_meal, name="service_meal"),
    path('', views.home, name="home"),
    path('about/', views.about, name="about"),
    path('team/', views.team, name="team"),
    # path('booking/', views.booking, name="booking"),
    path('contact/', views.contact, name="contact"),
    path('testimonial/', views.testimonial, name="testimonial"),
]