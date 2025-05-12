from django.core.management.base import BaseCommand
from django.utils import timezone
import pytz
from datetime import timedelta, datetime

from ass2.models import Airport, Aircraft, Flight, Route, Booking

class Command(BaseCommand):
    help = 'Init the database with initial data'
    
    def handle(self, *args, **options):
        self.stdout.write("Initializing the database...\n")
        
        # Only run this if the database is empty
        if Airport.objects.exists():
            self.stdout.write(self.style.WARNING("Database already initialized. Skipping...\n"))
            return
        
        self.create_airports()
        self.create_aircraft()
        self.create_routes()
        self.create_flights()
        
        # self.create_bookings()
        
        self.stdout.write(self.style.SUCCESS("Database initialized successfully.\n"))
        
    def create_airports(self):
        self.stdout.write("Creating airports...\n")
        
        self.airports = {}
        
        self.airports['dairy_flat'] = Airport.objects.create(
            airport_code='NZNE',
            airport_name='Dairy Flat',
            airport_location='North Shore, Auckland, New Zealand',
            airport_timezone='Pacific/Auckland',
            airport_latitude=-36.656666,
            airport_longitude=174.655278
        )
        
        self.airports['melbourne'] = Airport.objects.create(
            airport_code='YMML',
            airport_name='Tullamarine International Airport',
            airport_location='Melbourne, Victoria, Australia',
            airport_timezone='Australia/Melbourne',
            airport_latitude=-37.673332,
            airport_longitude=144.843333
        )
        
        self.airports['rotorua'] = Airport.objects.create(
            airport_code='NZRO',
            airport_name='Rotorua International Airport',
            airport_location='Rotorua, Bay of Plenty, New Zealand',
            airport_timezone='Pacific/Auckland',
            airport_latitude=-38.109166,
            airport_longitude=176.317222
        )
        
        self.airports['chatham'] = Airport.objects.create(
            airport_code='NZCI',
            airport_name='Tuuta Airport',
            airport_location='Waitangi, Chatham Islands, New Zealand',
            airport_timezone='Pacific/Chatham',
            airport_latitude=-43.809999,
            airport_longitude=-176.457221
        )
        
        self.airports['great_barrier'] = Airport.objects.create(
            airport_code='NZGB',
            airport_name='Claris Airport',
            airport_location='Great Barrier Island, Auckland, New Zealand',
            airport_timezone='Pacific/Auckland',
            airport_latitude=-36.241388,
            airport_longitude=175.471944
        )
        
        self.airports['tekapo'] = Airport.objects.create(
            airport_code='NZTL',
            airport_name='Lake Tekapo Airport',
            airport_location='Tekapo, Canterbury, New Zealand',
            airport_timezone='Pacific/Auckland',
            airport_latitude=-44.004999,
            airport_longitude=170.441667
        )
        
        self.stdout.write(f'Created {len(self.airports)} airports')
    
    def create_aircraft(self):
        self.stdout.write('Creating aircraft...')
    
        self.aircraft = {}
        
        self.aircraft['syberjet'] = Aircraft.objects.create(
            craft_type='SyberJet SJ30i',
            craft_capacity=6,
            craft_id='ID-SJ30',
            craft_remaining_capacity=6,  
            craft_status='Available',
            craft_location=self.airports['dairy_flat']
        )
        
        self.aircraft['cirrus1'] = Aircraft.objects.create(
            craft_type='Cirrus SF50',
            craft_capacity=4,
            craft_id='ID-SF51',
            craft_remaining_capacity=4,  
            craft_status='Available',
            craft_location=self.airports['dairy_flat']
        )
        
        self.aircraft['cirrus2'] = Aircraft.objects.create(
            craft_type='Cirrus SF50',
            craft_capacity=4,
            craft_id='ID-SF52',
            craft_remaining_capacity=4,  
            craft_status='Available',
            craft_location=self.airports['dairy_flat']
        )
        
        self.aircraft['hondajet1'] = Aircraft.objects.create(
            craft_type='HondaJet Elite',
            craft_capacity=5,
            craft_id='ID-HJ01',
            craft_remaining_capacity=5,  
            craft_status='Available',
            craft_location=self.airports['dairy_flat']
        )
        
        self.aircraft['hondajet2'] = Aircraft.objects.create(
            craft_type='HondaJet Elite',
            craft_capacity=5,
            craft_id='ID-HJ02',
            craft_remaining_capacity=5, 
            craft_status='Available',
            craft_location=self.airports['dairy_flat']
        )
        
        self.stdout.write(f'Created {len(self.aircraft)} aircraft')
    
    """
     The airline operates a weekly timetable with the following routes from Dairy Flat.
 • Aweekly “prestige” service to Melbourne using the SyberJet aircraft. The outbound
 f
 light departs Dairy Flat on Friday mid-morning with the return inbound flight de
parting Melbourne on Sunday mid-afternoon (their time).
 • Ashuttle service to Rotorua using one of the Cirrus jets. These operate twice every
 weekday Monday–Friday. The first flight departs Dairy Flat early morning with the
 return flight departing from Rotorua soon after. After turnaround, the next flight
 departs Dairy Flat late afternoon, with the return flight departing Rotorua in the
 evening.
 • Athree times weekly service to Claris airport in Great Barrier Island using the other
 Cirrus. The outbound flight departs Dairy Flat in the morning every Monday, Wednes
day, and Friday. The return flight departs Great Barrier Island in the morning every
 Tuesday, Thursday, and Saturday.
 • A twice weekly service to Tuuta Airport in the Chatham Islands using one of the
 HondaJets. The outbound flights depart Dairy Flat on Tuesday and Friday, with the
 return flights departing Tuuta on Wednesday and Saturday.
 • Aweeklyservice to Lake Tekapo in the South Island using the other HondaJet. Departs
 Dairy Flat on Monday with the return flight departing Tekapo on Tuesday.

    """
    def create_routes(self):
        self.stdout.write('Creating routes...')
        
        self.routes = {}
        
        # Melbourne route - Prestige service
        self.routes['melbourne'] = Route.objects.create(
            route_type='Prestige',
            route_frequency=7,  # Weekly
            route_price=1200.00,
            route_origin=self.airports['dairy_flat'],
            route_destination=self.airports['melbourne'],
            route_duration=4.00, 
            route_return_duration=3.50,
            route_aircraft=self.aircraft['syberjet']
        )
        
        # Rotorua route - Shuttle service
        self.routes['rotorua'] = Route.objects.create(
            route_type='Shuttle',
            route_frequency=1,  # Daily
            route_price=350.00,
            route_origin=self.airports['dairy_flat'],
            route_destination=self.airports['rotorua'],
            route_duration=1.00, 
            route_return_duration=1.00,
            route_aircraft=self.aircraft['cirrus1']
        )
        
        # Great Barrier Island route
        self.routes['great_barrier'] = Route.objects.create(
            route_type='Island',
            route_frequency=2,  # 3 times a week
            route_price=180.00,
            route_origin=self.airports['dairy_flat'],
            route_destination=self.airports['great_barrier'],
            route_duration=0.50, 
            route_return_duration=0.50,
            route_aircraft=self.aircraft['cirrus2']
        )
        
        # Chatham Islands route
        self.routes['chatham'] = Route.objects.create(
            route_type='Island',
            route_frequency=3,  # Twice a week
            route_price=750.00,
            route_origin=self.airports['dairy_flat'],
            route_destination=self.airports['chatham'],
            route_duration=2.00, 
            route_return_duration=2.50,
            route_aircraft=self.aircraft['hondajet1']
        )
        
        # Lake Tekapo route
        self.routes['tekapo'] = Route.objects.create(
            route_type='Scenic',
            route_frequency=7,  # Weekly
            route_price=600.00,
            route_origin=self.airports['dairy_flat'],
            route_destination=self.airports['tekapo'],
            route_duration=2.00, 
            route_return_duration=2.00,
            route_aircraft=self.aircraft['hondajet2']
        )
        
        self.stdout.write(f'Created {len(self.routes)} routes')
    
    def create_flights(self):
        self.stdout.write('Creating flights...')
        flights_created = 0
        
        # Create 2 weeks of flights starting from the next Monday
        today = timezone.now().date()
        days_until_monday = (0 - today.weekday()) % 7
        if days_until_monday == 0:
            days_until_monday = 7  # If today is Monday, start from next Monday
        
        start_date = today + timedelta(days=days_until_monday)
        
        # Helper function to create datetime with proper timezone
        def make_datetime(date, hour, minute=0, tz_str='Pacific/Auckland'):
            """Create a timezone-aware datetime"""
            try:
                tz = pytz.timezone(tz_str)
                naive_dt = datetime.combine(date, datetime.min.time().replace(hour=hour, minute=minute))
                return tz.localize(naive_dt)
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error creating datetime: {e}"))
                # Fallback to default timezone
                return timezone.make_aware(datetime.combine(date, datetime.min.time().replace(hour=hour, minute=minute)))
        
        # Function to calculate arrival times
        def calculate_arrival_time(departure_time, duration_hours, destination_timezone_str):
            """Calculate arrival time based on departure time and duration"""
            try:
                # Add duration
                arrival_time = departure_time + timedelta(hours=duration_hours)
                # Convert to destination timezone
                dest_tz = pytz.timezone(destination_timezone_str)
                return arrival_time.astimezone(dest_tz)
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error calculating arrival time: {e}"))
                # Return without timezone conversion as fallback
                return departure_time + timedelta(hours=duration_hours)
        
        # Generate flight schedules
        for week in range(2): #We can adjust this to increase the data volume, i.e. more weeks,  if needed, Ive kept it at 2 for testing purposes
            week_start = start_date + timedelta(days=7*week)
            
            # Melbourne flights (Friday out, Sunday return)
            friday = week_start + timedelta(days=4)  # Friday
            sunday = week_start + timedelta(days=6)  # Sunday
            
            # Create outbound Melbourne flight
            mel_departure_time = make_datetime(friday, 10, 0, 'Pacific/Auckland')
            mel_arrival_time = calculate_arrival_time(
                mel_departure_time, 
                self.routes['melbourne'].route_duration, 
                'Australia/Melbourne'
            )
            
            Flight.objects.create(
                flight_number=f'DF101-{friday.strftime("%Y%m%d")}',
                flight_route=self.routes['melbourne'],
                flight_origin=self.airports['dairy_flat'],
                flight_destination=self.airports['melbourne'],
                flight_departure_time=mel_departure_time,
                flight_arrival_time=mel_arrival_time,
                flight_aircraft=self.aircraft['syberjet'],
                flight_price=self.routes['melbourne'].route_price
            )
            flights_created += 1
            
            # Create return Melbourne flight
            mel_return_departure_time = make_datetime(sunday, 15, 0, 'Australia/Melbourne')
            mel_return_arrival_time = calculate_arrival_time(
                mel_return_departure_time, 
                self.routes['melbourne'].route_return_duration, 
                'Pacific/Auckland'
            )
            
            Flight.objects.create(
                flight_number=f'DF102-{sunday.strftime("%Y%m%d")}',
                flight_route=self.routes['melbourne'],
                flight_origin=self.airports['melbourne'],
                flight_destination=self.airports['dairy_flat'],
                flight_departure_time=mel_return_departure_time,
                flight_arrival_time=mel_return_arrival_time,
                flight_aircraft=self.aircraft['syberjet'],
                flight_price=self.routes['melbourne'].route_price
            )
            flights_created += 1
            
            # Add Rotorua shuttle flights (weekdays)
            for day_offset in range(5):  # Monday to Friday
                current_date = week_start + timedelta(days=day_offset)
                
                # Morning flight to Rotorua
                rot_departure_time = make_datetime(current_date, 8, 0, 'Pacific/Auckland')
                rot_arrival_time = calculate_arrival_time(
                    rot_departure_time, 
                    self.routes['rotorua'].route_duration, 
                    'Pacific/Auckland'
                )
                
                Flight.objects.create(
                    flight_number=f'DF201-{current_date.strftime("%Y%m%d")}',
                    flight_route=self.routes['rotorua'],
                    flight_origin=self.airports['dairy_flat'],
                    flight_destination=self.airports['rotorua'],
                    flight_departure_time=rot_departure_time,
                    flight_arrival_time=rot_arrival_time,
                    flight_aircraft=self.aircraft['cirrus1'],
                    flight_price=self.routes['rotorua'].route_price
                )
                flights_created += 1
                
                # Return morning flight from Rotorua
                rot_return_departure_time = make_datetime(current_date, 9, 30, 'Pacific/Auckland')
                rot_return_arrival_time = calculate_arrival_time(
                    rot_return_departure_time, 
                    self.routes['rotorua'].route_return_duration, 
                    'Pacific/Auckland'
                )
                
                Flight.objects.create(
                    flight_number=f'DF202-{current_date.strftime("%Y%m%d")}',
                    flight_route=self.routes['rotorua'],
                    flight_origin=self.airports['rotorua'],
                    flight_destination=self.airports['dairy_flat'],
                    flight_departure_time=rot_return_departure_time,
                    flight_arrival_time=rot_return_arrival_time,
                    flight_aircraft=self.aircraft['cirrus1'],
                    flight_price=self.routes['rotorua'].route_price
                )
                flights_created += 1
                
                # Afternoon flight to Rotorua
                rot_afternoon_departure_time = make_datetime(current_date, 17, 0, 'Pacific/Auckland')
                rot_afternoon_arrival_time = calculate_arrival_time(
                    rot_afternoon_departure_time,
                    self.routes['rotorua'].route_duration,
                    'Pacific/Auckland'
                )
                
                Flight.objects.create(
                    flight_number=f'DF203-{current_date.strftime("%Y%m%d")}',
                    flight_route=self.routes['rotorua'],
                    flight_origin=self.airports['dairy_flat'],
                    flight_destination=self.airports['rotorua'],
                    flight_departure_time=rot_afternoon_departure_time,
                    flight_arrival_time=rot_afternoon_arrival_time,
                    flight_aircraft=self.aircraft['cirrus1'],
                    flight_price=self.routes['rotorua'].route_price
                )
                flights_created += 1
                
                # Return afternoon flight from Rotorua
                rot_afternoon_return_departure_time = make_datetime(current_date, 18, 30, 'Pacific/Auckland')
                rot_afternoon_return_arrival_time = calculate_arrival_time(
                    rot_afternoon_return_departure_time,
                    self.routes['rotorua'].route_return_duration,
                    'Pacific/Auckland'
                )
                
                Flight.objects.create(
                    flight_number=f'DF204-{current_date.strftime("%Y%m%d")}',
                    flight_route=self.routes['rotorua'],
                    flight_origin=self.airports['rotorua'],
                    flight_destination=self.airports['dairy_flat'],
                    flight_departure_time=rot_afternoon_return_departure_time,
                    flight_arrival_time=rot_afternoon_return_arrival_time,
                    flight_aircraft=self.aircraft['cirrus1'],
                    flight_price=self.routes['rotorua'].route_price
                )
                flights_created += 1
            
            # Great Barrier Island flights
            for day_offset in range(6):  # Monday to Saturday
                current_date = week_start + timedelta(days=day_offset)
                
                # Monday, Wednesday, and Friday flights to Great Barrier Island
                if day_offset in [0, 2, 4]:  # Monday, Wednesday, Friday
                    gb_departure_time = make_datetime(current_date, 10, 0, 'Pacific/Auckland')
                    gb_arrival_time = calculate_arrival_time(
                        gb_departure_time,
                        self.routes['great_barrier'].route_duration,
                        'Pacific/Auckland'
                    )
                    
                    Flight.objects.create(
                        flight_number=f'DF301-{current_date.strftime("%Y%m%d")}',
                        flight_route=self.routes['great_barrier'],
                        flight_origin=self.airports['dairy_flat'],
                        flight_destination=self.airports['great_barrier'],
                        flight_departure_time=gb_departure_time,
                        flight_arrival_time=gb_arrival_time,
                        flight_aircraft=self.aircraft['cirrus2'],
                        flight_price=self.routes['great_barrier'].route_price
                    )
                    flights_created += 1
                
                # Tuesday, Thursday, Saturday return flights from Great Barrier
                if day_offset in [1, 3, 5]:  # Tuesday, Thursday, Saturday
                    gb_return_departure_time = make_datetime(current_date, 10, 0, 'Pacific/Auckland')
                    gb_return_arrival_time = calculate_arrival_time(
                        gb_return_departure_time,
                        self.routes['great_barrier'].route_return_duration,
                        'Pacific/Auckland'
                    )
                    
                    Flight.objects.create(
                        flight_number=f'DF302-{current_date.strftime("%Y%m%d")}',
                        flight_route=self.routes['great_barrier'],
                        flight_origin=self.airports['great_barrier'],
                        flight_destination=self.airports['dairy_flat'],
                        flight_departure_time=gb_return_departure_time,
                        flight_arrival_time=gb_return_arrival_time,
                        flight_aircraft=self.aircraft['cirrus2'],
                        flight_price=self.routes['great_barrier'].route_price
                    )
                    flights_created += 1
                    
            # Chatham Islands flights
            for day_offset in range(7):  # Full week
                current_date = week_start + timedelta(days=day_offset)
                
                # Tuesday and Friday flights to Chatham Islands
                if day_offset in [1, 4]:  # Tuesday, Friday
                    ch_departure_time = make_datetime(current_date, 9, 0, 'Pacific/Auckland')
                    ch_arrival_time = calculate_arrival_time(
                        ch_departure_time,
                        self.routes['chatham'].route_duration,
                        'Pacific/Chatham'
                    )
                    
                    Flight.objects.create(
                        flight_number=f'DF401-{current_date.strftime("%Y%m%d")}',
                        flight_route=self.routes['chatham'],
                        flight_origin=self.airports['dairy_flat'],
                        flight_destination=self.airports['chatham'],
                        flight_departure_time=ch_departure_time,
                        flight_arrival_time=ch_arrival_time,
                        flight_aircraft=self.aircraft['hondajet1'],
                        flight_price=self.routes['chatham'].route_price
                    )
                    flights_created += 1
                
                # Wednesday and Saturday return flights from Chatham Islands
                if day_offset in [2, 5]:  # Wednesday, Saturday
                    ch_return_departure_time = make_datetime(current_date, 10, 0, 'Pacific/Chatham')
                    ch_return_arrival_time = calculate_arrival_time(
                        ch_return_departure_time,
                        self.routes['chatham'].route_return_duration,
                        'Pacific/Auckland'
                    )
                    
                    Flight.objects.create(
                        flight_number=f'DF402-{current_date.strftime("%Y%m%d")}',
                        flight_route=self.routes['chatham'],
                        flight_origin=self.airports['chatham'],
                        flight_destination=self.airports['dairy_flat'],
                        flight_departure_time=ch_return_departure_time,
                        flight_arrival_time=ch_return_arrival_time,
                        flight_aircraft=self.aircraft['hondajet1'],
                        flight_price=self.routes['chatham'].route_price
                    )
                    flights_created += 1
            
            # Lake Tekapo flights
            # Monday outbound
            tekapo_departure_time = make_datetime(week_start, 10, 0, 'Pacific/Auckland')  # Monday
            tekapo_arrival_time = calculate_arrival_time(
                tekapo_departure_time,
                self.routes['tekapo'].route_duration,
                'Pacific/Auckland'
            )
            
            Flight.objects.create(
                flight_number=f'DF501-{week_start.strftime("%Y%m%d")}',
                flight_route=self.routes['tekapo'],
                flight_origin=self.airports['dairy_flat'],
                flight_destination=self.airports['tekapo'],
                flight_departure_time=tekapo_departure_time,
                flight_arrival_time=tekapo_arrival_time,
                flight_aircraft=self.aircraft['hondajet2'],
                flight_price=self.routes['tekapo'].route_price
            )
            flights_created += 1
            
            # Tuesday return from Tekapo
            tuesday = week_start + timedelta(days=1)
            tekapo_return_departure_time = make_datetime(tuesday, 10, 0, 'Pacific/Auckland')
            tekapo_return_arrival_time = calculate_arrival_time(
                tekapo_return_departure_time,
                self.routes['tekapo'].route_return_duration,
                'Pacific/Auckland'
            )
            
            Flight.objects.create(
                flight_number=f'DF502-{tuesday.strftime("%Y%m%d")}',
                flight_route=self.routes['tekapo'],
                flight_origin=self.airports['tekapo'],
                flight_destination=self.airports['dairy_flat'],
                flight_departure_time=tekapo_return_departure_time,
                flight_arrival_time=tekapo_return_arrival_time,
                flight_aircraft=self.aircraft['hondajet2'],
                flight_price=self.routes['tekapo'].route_price
            )
            flights_created += 1
            
        self.stdout.write(f'Created {flights_created} flights')