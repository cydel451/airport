from django.urls import path
from . import views

urlpatterns = [
    path('', views.plane_list, name='plane_list'),
    path('plane/<str:pk>/', views.flight_detail, name='flight_detail'),
    path('plane/<str:pk>/?<str:message>', views.flight_detail, name='flight_detail_mes'),
    path('crash/', views.crash, name='crash')
]