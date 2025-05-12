from django.db import models
from django.utils import timezone
import uuid

# Models for the database
class Flight(models.Model):
    flight_number = models.CharField(max_length=10)
    flight_route = models.ForeignKey('Route', on_delete=models.CASCADE, related_name='flights')
    flight_origin = models.ForeignKey('Airport', on_delete=models.CASCADE, related_name='departures')
    flight_destination = models.ForeignKey('Airport', on_delete=models.CASCADE, related_name='arrivals')
    flight_departure_time = models.DateTimeField()
    flight_arrival_time = models.DateTimeField()
    flight_aircraft = models.ForeignKey('Aircraft', on_delete=models.CASCADE)
    flight_price = models.DecimalField(max_digits=8, decimal_places=2)
    flight_status = models.CharField(max_length=50, default='Scheduled', 
                                    help_text="Status of the flight (e.g., Scheduled, Delayed, Cancelled)")
    
    class Meta:
        ordering = ['flight_departure_time']
    
    def __str__(self):
        return f"{self.flight_number}: {self.flight_origin.airport_code} to {self.flight_destination.airport_code}"
    
    @property
    def duration(self):
        """Calculate flight duration in hours and minutes"""
        duration = self.flight_arrival_time - self.flight_departure_time
        hours, remainder = divmod(duration.total_seconds(), 3600)
        minutes, _ = divmod(remainder, 60)
        return f"{int(hours)}h {int(minutes)}m"
    
    @property
    def booked_seats(self):
        """Count number of confirmed bookings for this flight"""
        return self.booking_set.filter(booking_status='Confirmed').count()
    
    @property
    def available_seats(self):
        """Calculate number of available seats"""
        return self.flight_aircraft.craft_capacity - self.booked_seats
    
    @property
    def is_full(self):
        """Check if flight is fully booked"""
        return self.available_seats <= 0
    
    @property
    def is_bookable(self):
        """Check if flight can be booked (not full, not departed, not cancelled)"""
        return (not self.is_full and 
                self.flight_status not in ['Cancelled', 'Completed'] and
                self.flight_departure_time > timezone.now())
    
    
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
    craft_remaining_capacity = models.IntegerField(help_text="Remaining capacity of the aircraft")
    craft_location = models.ForeignKey('Airport', on_delete=models.CASCADE, related_name='aircraft_location')
    craft_status = models.CharField(max_length=50, help_text="Status of the aircraft (e.g., Available, In Maintenance)")
    #MAYBE: MAintenance time, seat map? 
    
    def __str__(self):
        return f"{self.craft_type} ({self.craft_id})"

class Airport(models.Model):
    """
    Airport model to store airport information.
    """
    airport_code = models.CharField(max_length=10, unique=True, help_text="Unique identifier for the airport eg INV") 
    airport_name = models.CharField(max_length=100, help_text="Name of airport")
    airport_location = models.CharField(max_length=100, help_text="Location")
    airport_timezone = models.CharField(max_length=50, help_text="Timezone of the airport")
    airport_latitude = models.DecimalField(max_digits=9, decimal_places=6, help_text="Latitude of the airport")
    airport_longitude = models.DecimalField(max_digits=9, decimal_places=6, help_text="Longitude of the airport")
    
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
    route_duration = models.DecimalField(max_digits=4, decimal_places=2, help_text="Typical flight duration in hours") 
    route_return_duration = models.DecimalField(max_digits=4, decimal_places=2, help_text="Return flight duration in hours", null=True, blank=True) 
    route_aircraft = models.ForeignKey('Aircraft', on_delete=models.CASCADE, related_name='route_aircraft')
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
    booking_id = models.UUIDField(default=uuid.uuid4, editable=False,unique=True,
                                  help_text="Unique booking reference number")
    booking_flight = models.ForeignKey('Flight', on_delete=models.CASCADE)
    booking_customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    booking_created_at = models.DateTimeField(auto_now_add=True, help_text="Date and time when booking was made")
    booking_requests = models.CharField(max_length=100, help_text="Special requests or notes")
    booking_status = models.CharField(max_length=50, default='Pending', help_text="Status of the booking (e.g., Confirmed, Cancelled)")
    booking_date = models.DateField(default=timezone.now, help_text="Date of the flight")
    
    def __str__(self):
        return f"Booking #{self.booking_id}: {self.customer.first_name} on {self.flight.flight_number}"
    
class Payment(models.Model):
    """
    Payment model to store payment information for bookings.
    """
    payment_booking = models.ForeignKey('Booking', on_delete=models.CASCADE)
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2, help_text="Payment amount")
    payment_date = models.DateTimeField(auto_now_add=True, help_text="Date and time of the payment")
    payment_status = models.CharField(max_length=50, default='Pending', help_text="Status of the payment (e.g., Completed, Failed)")
    
    def __str__(self):
        return f"Payment #{self.id} for Booking #{self.booking.id}"