"""
URL configuration for ass2 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from ass2 import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Main site routes
    path('', views.homepage, name='homepage'),
    path('about/', views.about, name='about'),
    
    # Flight search and booking
    path('flights/', views.flight_search, name='flight_search'),
    path('booking/create/<int:flight_id>/', views.booking_create, name='booking_create'),
    path('booking/confirmation/<int:booking_id>/', views.booking_confirmation, name='booking_confirmation'),
    path('booking/lookup/', views.booking_lookup, name='booking_lookup'),
    path('booking/cancel/<int:booking_id>/', views.booking_cancel, name='booking_cancel'),
    
]