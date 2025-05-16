from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.utils import timezone  # Add this import for timezone
from django.core.paginator import Paginator
from django.db.models import Q  # Add this for Q objects
import datetime
import uuid

from ass2.models import Airport, Aircraft, Flight, Route, Customer, Booking, Payment

# Create your views here.
def hello(request):
    text = '<h1>Welcome to my app!</h1>Nice to see you here'
    return HttpResponse(text)

def homepage(request):
    return render(request, 'homepage.html', {'name': 'Zak'})

# def formjs(request):
#     return render(request, 'formjs.html', {})

# About us page view
def about(request):
    return render(request, 'about.html')
#Dated and unused
# def bookings(request):
#     """
#     #Create a booking model instance
#     booking_flight = models.ForeignKey('Flight', on_delete=models.CASCADE)
#     booking_customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
#     booking_created_at = models.DateTimeField(auto_now_add=True, help_text="Date and time when booking was made")
#     booking_requests = models.CharField(max_length=100, help_text="Special requests or notes")
#     booking_status = models.CharField(max_length=50, default='Pending', help_text="Status of the booking (e.g., Confirmed, Cancelled)")
#     booking_date = models.DateField(default=timezone.now, help_text="Date of the flight")
#     """
#     b = Booking(
#          booking_flight = request.POST['booking_flight'],
#          booking_customer = request.POST['booking_customer'],
#          #booking_created_at = request.POST['booking_created_at'],
#          booking_requests = request.POST['booking_requestes'],
#          booking_status = request.POST['booking_status'],  
#          booking_date = request.POST['booking_date'])
#     #Save to the database
#     b.save()
#     #Return a Json response containing the details
#     return JsonResponse({
#             'booking_flight': request.POST['booking_flight'], 
#             'booking_customer': request.POST['booking_customer'], 
#             'booking_created_at': b.booking_created_at.isoformat(), 
#             'booking_requests': request.POST['booking_requests'],  
#             'booking_status': request.POST['booking_status'],
#             'booking_date': request.POST['booking_date'],
#             'status': 'success'
#     })
    
#     return render(request, 'booking_form.html', {})

# def aircraft(request):
#     return render(request, 'aircraft.html', {})

def flight_search(request):
    search_performed = False
    flights = []
    search_params = {}
    
    if request.GET:
        search_performed = True
        origin = request.GET.get('origin', 'NZNE')  # Default to Dairy Flat
        destination = request.GET.get('destination')
        departure_date_str = request.GET.get('departure_date')
        passengers = int(request.GET.get('passengers', 1))
        show_all = request.GET.get('show_all') == 'true'
        
        # Build query
        query = Q()
        
        # Filter by origin
        if origin:
            query &= Q(flight_origin__airport_code=origin)
            try:
                origin_airport = Airport.objects.get(airport_code=origin)
                search_params['origin_name'] = origin_airport.airport_name
            except Airport.DoesNotExist:
                pass
        
        # Filter by destination
        if destination:
            query &= Q(flight_destination__airport_code=destination)
            try:
                destination_airport = Airport.objects.get(airport_code=destination)
                search_params['destination_name'] = destination_airport.airport_name
            except Airport.DoesNotExist:
                pass
        
        # Filter by date if provided
        if departure_date_str:
            try:
                departure_date = datetime.datetime.strptime(departure_date_str, '%Y-%m-%d').date()
                search_params['departure_date'] = departure_date
                
                # Get flights on the selected date
                query &= Q(flight_departure_time__date=departure_date)
            except ValueError:
                # Invalid date format, ignore date filter
                pass
        
        # Ensure we only show future flights that are not cancelled
        query &= Q(flight_departure_time__gt=timezone.now()) 
        query &= ~Q(flight_status='Cancelled') 
        
        # Get flights with available seats
        flights = Flight.objects.filter(query).order_by('flight_departure_time')
        
        # Filter flights that have enough seats
        flights = [flight for flight in flights if flight.available_seats >= passengers]
        
        # Paginate results
        paginator = Paginator(flights, 10)  # Show 10 flights per page
        page_number = request.GET.get('page', 1)
        flights = paginator.get_page(page_number)
    
    return render(request, 'flight_search.html', {
        'flights': flights,
        'search_performed': search_performed,
        'search_params': search_params,
        'origin': request.GET.get('origin', 'NZNE'),
        'destination': request.GET.get('destination', ''),
        'departure_date': request.GET.get('departure_date', timezone.now().date()),
        'passengers': int(request.GET.get('passengers', 1))
    })
    
def booking_create(request, flight_id):
        flight = get_object_or_404(Flight, id=flight_id)
       
        # Check if flight is full or in the past
        if not flight.is_bookable:
            messages.error(request, "This flight is no longer available for booking.")
            return redirect('flight_search')
        
        if request.method == 'POST':
            # Create or get customer
            customer_email = request.POST.get('customer_email')
            
            try:
                customer = Customer.objects.get(customer_email=customer_email)
                # Update customer details
                customer.customer_first_name = request.POST.get('customer_first_name')
                customer.customer_last_name = request.POST.get('customer_last_name')
                customer.customer_phone = request.POST.get('customer_phone')
                customer.save()
            except Customer.DoesNotExist:
                # Create new customer
                customer = Customer.objects.create(
                    customer_email=request.POST.get('customer_email'),
                    customer_first_name=request.POST.get('customer_first_name'),
                    customer_last_name=request.POST.get('customer_last_name'),
                    customer_phone=request.POST.get('customer_phone')
                )
            
            # Create booking
            booking = Booking.objects.create(
                booking_flight=flight,
                booking_customer=customer,
                booking_requests=request.POST.get('booking_requests', ''),
                booking_status='Confirmed',
                booking_date=flight.flight_departure_time.date()
            )
            
            # Create payment record
            payment = Payment.objects.create(
                payment_booking=booking,
                payment_amount=flight.flight_price,
                payment_status='Completed'
            )
            
            # Redirect to confirmation page
            return redirect('booking_confirmation', booking_id=booking.id)
    
        
        total_price = flight.flight_price 
        
        return render(request, 'booking_create.html', {
            'flight': flight,
            'total_price': total_price
        })

# Booking confirmation view
def booking_confirmation(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    payment = Payment.objects.filter(payment_booking=booking).first()
    
    return render(request, 'booking_confirmation.html', {
        'booking': booking,
        'payment': payment
    })

# Booking lookup view
def booking_lookup(request):
    booking = None
    error_message = None
    
    if request.method == 'POST':
        booking_id = request.POST.get('booking_id')
        email = request.POST.get('email')
        
        try:
            # Try to find the booking
            booking = Booking.objects.get(id=booking_id)
            
            # Verify email matches
            if booking.booking_customer.customer_email.lower() != email.lower():
                error_message = "The email address doesn't match our records for this booking."
                booking = None
        except Booking.DoesNotExist:
            error_message = "We couldn't find a booking with that reference number."
    
    return render(request, 'booking_lookup.html', {
        'booking': booking,
        'error_message': error_message,
        'booking_id': request.POST.get('booking_id', ''),
        'email': request.POST.get('email', '')
    })

# Cancel booking view
def booking_cancel(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    
    # Only allow cancellation of confirmed bookings
    if booking.booking_status == 'Confirmed':
        booking.booking_status = 'Cancelled'
        booking.save()
    # if booking.payment_status == 'C':
    #     booking.delete()
        
        messages.success(request, "Your booking has been cancelled.")
    else:
        messages.error(request, "This booking cannot be cancelled.")
    
    return redirect('booking_lookup')

