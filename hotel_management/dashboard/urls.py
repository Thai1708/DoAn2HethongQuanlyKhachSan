from django.urls import path

from . import views

app_name = 'booking'

urlpatterns = [
    path('daily_report/', views.daily_report, name='daily_report'),
]