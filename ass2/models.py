
from django.db import models

from django.utils import timezone

# Models for the database
class Flight(models.Model):
   
    flight_number = models.CharField(max_length=10)
    flight_origin = models.ForeignKey('Airport', on_delete=models.CASCADE, related_name='departures')
    flight_destination = models.ForeignKey('Airport', on_delete=models.CASCADE, related_name='arrivals')
    flight_departure_time = models.DateTimeField()
    flight_arrival_time = models.DateTimeField()
    flight_aircraft = models.ForeignKey('Aircraft', on_delete=models.CASCADE)
    fligh_price = models.DecimalField(max_digits=8, decimal_places=2)
    
    def __str__(self):
        return self.flight_number
    
class Aircraft(models.Model):
    """
    Aircraft model representing planes in the system.
    Used for flight assignments and capacity planning.
    Info:
    The pride of the fleet is a SyberJet SJ30i which can
    carry 6 passengers in luxury. Other aircraft are: two Cirrus SF50 jets that take 4 passengers
    each and two HondaJet Elite planes that can take 5 passengers each.
    """
    craft_type = models.CharField(max_length=100, help_text="Type/model of the aircraft")
    craft_capacity = models.IntegerField(help_text="Maximum passenger capacity")
    craft_id = models.CharField(max_length=100, unique=True, help_text="Registration number of the aircraft")
    
    def __str__(self):
        return f"{self.craft_type} ({self.craft_id})"

class Airport(models.Model):
    """
    Airport model to store airport information.
    """
    airport_code = models.CharField(max_length=10, unique=True, help_text="Unique identifier for the airport eg INV") 
    airport_name = models.CharField(max_length=100, help_text="Name of airport")
    airport_location = models.CharField(max_length=100, help_text="Location")
    
    def __str__(self):
        return f"{self.airport_code} - {self.airport_name}"
    
class Route(models.Model):
    """
    Route model representing connections between airports.
    """
    route_type = models.CharField(max_length=100, help_text="Type of route prestige, shuttle etc")
    route_frequency = models.IntegerField(help_text="Frequency of the route in days")
    route_price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Price of the route")
    route_origin = models.ForeignKey('Airport', on_delete=models.CASCADE, related_name='route_origins')
    route_destination = models.ForeignKey('Airport', on_delete=models.CASCADE, related_name='route_destinations')
    route_distance = models.DecimalField(max_digits=10, decimal_places=2, help_text="Distance in kilometers/miles")
    
    def __str__(self):
        return f"{self.origin.airport_code} to {self.destination.airport_code} ({self.route_type})"
    
class Customer(models.Model):
    """
    Customer model to store customer information.
    """
    customer_email = models.EmailField(max_length=100, unique=True, help_text="Customer's email address")
    customer_first_name = models.CharField(max_length=100, help_text="Customer's first name")
    customer_last_name = models.CharField(max_length=100, help_text="Customer's last name")
    customer_phone = models.CharField(max_length=20, help_text="Customer's contact number")
    customer_loyalty_points = models.FloatField(default=0, help_text="Frequent flyer points")
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"
    
class Booking(models.Model):
    """
    Booking model to store flight bookings.
    """
    booking_flight = models.ForeignKey('Flight', on_delete=models.CASCADE)
    booking_customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    booking_created_at = models.DateTimeField(auto_now_add=True, help_text="Date and time when booking was made")
    booking_requestes = models.CharField(max_length=100, help_text="Special requests or notes")
    
    def __str__(self):
        return f"Booking #{self.id}: {self.customer.first_name} on {self.flight.flight_number}"