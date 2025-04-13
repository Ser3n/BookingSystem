# Import the Django models module for database model creation
from django.db import models
# Import timezone utilities for handling dates and times
from django.utils import timezone

# Models for the database

class Aircraft(models.Model):
    """
    Aircraft model representing planes in the system.
    Used for flight assignments and capacity planning.
 
he pride of the fleet is a SyberJet SJ30i which can
 carry 6 passengers in luxury. Other aircraft are: two Cirrus SF50 jets that take 4 passengers
 each and two HondaJet Elite planes that can take 5 passengers each.
    """
    # Store the type/model of aircraft (e.g., "Boeing 747", "Airbus A320")
    craft_type = models.CharField(max_length=100, help_text="Type/model of the aircraft")
    # Store the maximum number of passengers the aircraft can carry
    craft_capacity = models.IntegerField(help_text="Maximum passenger capacity")
    # Unique registration number or identifier for the specific aircraft
    craft_id = models.CharField(max_length=100, unique=True, help_text="Unique identifier for the aircraft")
    
    # String representation of the Aircraft object for admin interface and debugging
    def __str__(self):
        return f"{self.craft_type} ({self.craft_id})"

class Airports(models.Model):
    """
    Airport model to store airport information.
    Forms the nodes in the route network.
    # TODO: Add fields for airport code, name, location, etc.
    """
    
class Routes(models.Model):
    """
    Route model representing connections between airports.
    Defines possible flight paths in the network.
    # TODO: Add fields for origin, destination, distance, etc.
    """

