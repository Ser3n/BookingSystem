from django.core.management.base import BaseCommand
from django.utils import timezone
import pytz
from datetime import timedelta, datetime

from ass2.models import Airport, Aircraft, Flight, Route, Booking

class Command(BaseCommand):
    help = 'Init the database with initial data'
    
    def handle(self, *args, **options):
        self.stdout.write("Initializing the database...\n")
        
        #Only run this if the database is empty
        if Airport.objects.exists():
            self.stdout.write(self.style.WARNING("Database already initialized. Skipping...\n"))
            return
        
        self.create_airports()
        self.create_aircraft()
        self.create_routes()
        self.create_flights()
        
        #self.create_bookings()
        
        self.stdout.write(self.style.SUCCESS("Database initialized successfully.\n"))
        
    def create_airports(self):
        self.stdout.write("Creating airports...\n")
        
        #NZNE (Dairy Flat), YMML (Melbourne), NZRO (Rotorua), NZCI (Tuuta), Claris (NZGB), and Lake Tekapo (NZT
        #Mainland New Zealand (GMT+12), the Chatham Islands (GMT+12:45), and Melbourne (GMT+10).
        
        airport = {
            
            'dairy_flat': Airport.objects.create(
            airport_code='NZNE',
            airport_name='Dairy Flat',
            airport_location='North Shore, Auckland (Tamaki-makau-rau), New Zealand',
            airport_timezone='GMT+12',
            airport_latitude=-36.656666,
            airport_longitude=174.655278
            ),
            
           'melbourne': Airport.objects.create(
                airport_code='YMML',
                airport_name='Tullamarine International Airport',
                airport_location='Melbourne, Victoria, Australia',
                airport_timezone='GMT+10',
                airport_latitude=-37.673332,
                airport_longitude=144.843333
            ),
            'rotorua': Airport.objects.create(
                airport_code='NZRO',
                airport_name='Rotorua International Airport',
                airport_location='Rotorua, Bay of Plenty (Te Moana a Toi Te Huatahi), New Zealand',
                airport_timezone='GMT+12',
                airport_latitude=-38.109166,
                airport_longitude=176.317222
            ),
              'chatham': Airport.objects.create(
                airport_code='NZCI',
                airport_name='Tuuta Airport',
                airport_location='Waitangi, Chatham Islands (Wharekauri), New Zealand',
                airport_timezone='GMT+12:45',
                airport_latitude=-43.809999,
                airport_longitude=-176.457221
            ),
            'great_barrier': Airport.objects.create(
                airport_code='NZGB',
                airport_name='Claris Airport',
                airport_location='Great Barrier Island, Auckland (Tamaki-makau-rau), New Zealand',
                airport_timezone='GMT+12',
                airport_latitude=-36.241388,
                airport_longitude=175.471944
            ),
          
            'tekapo': Airport.objects.create(
                airport_code='NZTL',
                airport_name='Lake Tekapo Airport',
                airport_location='Tekapo, Canterbury (Waitaha), New Zealand',
                airport_timezone='GMT+12',
                airport_latitude=-44.004999,
                airport_longitude=170.441667
            )
        }
        
        self.airports = airport
        self.stdout.write(f'Created {len(airport)} airports')
    
    def create_aircraft(self):
        self.stdout.write('Creating aircraft...')
       
        aircraft = {
            'syberjet': Aircraft.objects.create(
                craft_type='SyberJet SJ30i',
                craft_capacity=6,
                craft_id='ID-SJ30',
                craft_remaining_capacity=6,
                craft_location=self.airports['dairy_flat'],
                craft_status='Available'
            ),
            'cirrus1': Aircraft.objects.create(
                craft_type='Cirrus SF50',
                craft_capacity=4,
                craft_id='ID-SF51',
                craft_remaining_capacity=4,
                craft_location=self.airports['dairy_flat'],
                craft_status='Available'
            ),
            'cirrus2': Aircraft.objects.create(
                craft_type='Cirrus SF50',
                craft_capacity=4,
                craft_id='ID-SF52',
                craft_remaining_capacity=4,
                craft_location=self.airports['dairy_flat'],
                craft_status='Available'
            ),
            'hondajet1': Aircraft.objects.create(
                craft_type='HondaJet Elite',
                craft_capacity=5,
                craft_id='ID-HJ01',
                craft_remaining_capacity=5,
                craft_location=self.airports['dairy_flat'],
                craft_status='Available'
            ),
            'hondajet2': Aircraft.objects.create(
                craft_type='HondaJet Elite',
                craft_capacity=5,
                craft_id='ID-HJ02',
                craft_remaining_capacity=5,
                craft_location=self.airports['dairy_flat'],
                craft_status='Available'
            )
        }
        self.aircraft = aircraft
        self.stdout.write(f'Created {len(aircraft)} aircraft')
    
    def create_routes(self):
        self.stdout.write('Creating routes...')
        routes = {
            """
            Aweekly “prestige” service to Melbourne using the SyberJet aircraft. The outbound
            flight departs Dairy Flat on Friday mid-morning with the return inbound flight de
            parting Melbourne on Sunday mid-afternoon (their time).
            """
            
            'melbourne': Route.objects.create(
                route_type='Prestige',
                route_frequency=7,  # Weekly
                route_price=1200.00,
                route_origin=self.airports['dairy_flat'],
                route_destination=self.airports['melbourne'],
                route_duration = 4.00, 
                route_return_duration = 3.50
            ),
            
            """
            A shuttle service to Rotorua using one of the Cirrus jets. These operate twice every
            weekday Monday–Friday. The first flight departs Dairy Flat early morning with the
            return flight departing from Rotorua soon after. After turnaround, the next flight
            departs Dairy Flat late afternoon, with the return flight departing Rotorua in the
            evening.
            """
            'rotorua': Route.objects.create(
                route_type='Shuttle',
                route_frequency=1,  # Daily
                route_price=350.00,
                route_origin=self.airports['dairy_flat'],
                route_destination=self.airports['rotorua'],
                route_duration = 1, 
                route_return_duration = 1
            ),
            
            """
            Athree times weekly service to Claris airport in Great Barrier Island using the other
            Cirrus. The outbound flight departs Dairy Flat in the morning every Monday, Wednes
            day, and Friday. The return flight departs Great Barrier Island in the morning every
            Tuesday, Thursday, and Saturday.
            """
            'great_barrier': Route.objects.create(
                route_type='Island',
                route_frequency=2,  # 3 times a week
                route_price=180.00,
                route_origin=self.airports['dairy_flat'],
                route_destination=self.airports['great_barrier'],
                 route_duration = .5, 
                route_return_duration = .5
            ),
            
            """
            A twice weekly service to Tuuta Airport in the Chatham Islands using one of the
             HondaJets. The outbound flights depart Dairy Flat on Tuesday and Friday, with the
            return flights departing Tuuta on Wednesday and Saturday.
            """
            'chatham': Route.objects.create(
                route_type='Island',
                route_frequency=3,  # Twice a week
                route_price=750.00,
                route_origin=self.airports['dairy_flat'],
                route_destination=self.airports['chatham'],
                route_duration = 2, 
                route_return_duration = 2.5
            ),
            
            """
             Aweeklyservice to Lake Tekapo in the South Island using the other HondaJet. Departs
             Dairy Flat on Monday with the return flight departing Tekapo on Tuesday
            """
            'tekapo': Route.objects.create(
                route_type='Scenic',
                route_frequency=7,  # Weekly
                route_price=600.00,
                route_origin=self.airports['dairy_flat'],
                route_destination=self.airports['tekapo'],
                route_duration = 2, 
                route_return_duration = 2
            )
        }
        self.routes = routes
        self.stdout.write(f'Created {len(routes)} routes')
    
    
    
        
    def create_flights(self):
        self.stdout.write('Creating flights...')
        flights_created = 0
        
        # Create 8 weeks of flights starting from the next Monday
        today = timezone.now().date()
        days_until_monday = (7 - today.weekday()) % 7
        if days_until_monday == 0:
            days_until_monday = 7  # If today is Monday, start from next Monday
        
        start_date = today + timedelta(days=days_until_monday)
        
         # Helper function to create datetime with proper timezone
        def make_datetime(date, hour , minute=0, airport=None):
            """Create a timezone-aware datetime based on an airport's timezone"""
            # Get the timezone object
            tz_str = airport.airport_timezone
           
            tz = pytz.timezone(tz_str)
            time = datetime.min.replace(hour=hour, minute=minute)
            # Create a naive datetime and localize it
            naive_dt = datetime.combine(date, time(hour=hour, minute=minute))
            return tz.localize(naive_dt)
        
        #Function to calculate arrival times
        def calculate_arrival_time(departure_time, duration, destination_aitport):
            #Calculate the arrival time based on the departure time and duration

            #Convert duration to Timedelta
            duration = timedelta(hours= duration)
            
            # Add duration to departure time 
            Arr_time_origin_timezone = departure_time + duration
            
            #Convert to destination timezone
            dest_timezone = pytz.timezone(destination_aitport.airport_timezone)
            arrival_time_dest_timezone = Arr_time_origin_timezone.astimezone(dest_timezone)
            
            return arrival_time_dest_timezone
            
        
            
        # Generate 8 weeks of flight schedules
        for week in range(8):
            week_start = start_date + timedelta(days=7*week)
            
            # Melbourne flights (Friday out, Sunday return)
            friday = week_start + timedelta(days=4)  # Friday
            sunday = week_start + timedelta(days=6)  # Sunday
            flight_departure_time = make_datetime(friday, 10, 0, self.airports['dairy_flat'])
            # Create outbound Melbourne flight
            Flight.objects.create(
                flight_number=f'DF101-{friday.strftime("%Y%m%d")}',
                flight_origin=self.airports['dairy_flat'],
                flight_destination=self.airports['melbourne'],
                flight_departure_time=make_datetime(friday, 10,0, self.airports['dairy_flat']),
                flight_arrival_time=calculate_arrival_time(flight_departure_time, self.routes['melbourne'].route_duration, self.airports['melbourne']),
                flight_aircraft=self.aircraft['syberjet'],
                fligh_price= self.routes['melbourne'].route_price
            )
            flights_created += 1
            
            flight_departure_time=make_datetime(sunday, 12,0, self.airports['melbourne'])
            
            # Create return Melbourne flight
            Flight.objects.create(
                flight_number=f'DF102-{sunday.strftime("%Y%m%d")}',
                flight_origin=self.airports['melbourne'],
                flight_destination=self.airports['dairy_flat'],
                flight_departure_time=make_datetime(sunday, 12,0, self.airports['melbourne']),
                flight_arrival_time=calculate_arrival_time(flight_departure_time, self.routes['melbourne'].route_duration_return, self.airports['melbourne']),
                flight_aircraft=self.aircraft['syberjet'],
                fligh_price=self.routes['melbourne'].route_price
            )
            flights_created += 1
            
            # Add Rotorua shuttle flights (weekdays)
            for day_offset in range(5):  # Monday to Friday
                current_date = week_start + timedelta(days=day_offset)
                
                flight_departure_time=make_datetime(current_date, 8, 0, self.airports['dairy_flat'])
                
                # Morning flight to Rotorua
                Flight.objects.create(
                    flight_number=f'DF201-{current_date.strftime("%Y%m%d")}',
                    flight_origin=self.airports['dairy_flat'],
                    flight_destination=self.airports['rotorua'],
                    flight_departure_time=make_datetime(current_date, 8, 0, self.airports['dairy_flat']),
                    flight_arrival_time=calculate_arrival_time(flight_departure_time, self.routes['rotorua'].route_duration_return, self.airports['rotorua']),
                    flight_aircraft=self.aircraft['cirrus1'],
                    fligh_price=self.routes['rotorua'].route_price
                )
                flights_created += 1
                
                flight_departure_time=make_datetime(current_date, 9, 30, self.airports['rotorua'])
                
                # Return morning flight from Rotorua
                Flight.objects.create(
                    flight_number=f'DF202-{current_date.strftime("%Y%m%d")}',
                    flight_origin=self.airports['rotorua'],
                    flight_destination=self.airports['dairy_flat'],
                    flight_departure_time=make_datetime(current_date, 9, 30, self.airports['rotorua']),
                    flight_arrival_time=calculate_arrival_time(flight_departure_time, self.routes['rotorua'].route_duration_return, self.airports['dairy_flat']),
                    flight_aircraft=self.aircraft['cirrus1'],
                    fligh_price=self.routes['rotorua'].route_price
                )
                flights_created += 1
                
                flight_departure_time=make_datetime(current_date, 17, 0, self.airports['dairy_flat'])
                # Afternoon flight to Rotorua
                Flight.objects.create(
                    flight_number=f'DF203-{current_date.strftime("%Y%m%d")}',
                    flight_origin=self.airports['dairy_flat'],
                    flight_destination=self.airports['rotorua'],
                    flight_departure_time=make_datetime(current_date, 17, 0, self.airports['dairy_flat']),
                    flight_arrival_time=calculate_arrival_time(flight_departure_time, self.routes['rotorua'].route_duration_return, self.airports['rotorua']),
                    flight_aircraft=self.aircraft['cirrus1'],
                    fligh_price=self.routes['rotorua'].route_price
                )
                flights_created += 1
                
                flight_departure_time=make_datetime(current_date, 20, 0, self.airports['rotorua'])
                # Return afternoon flight from Rotorua
                Flight.objects.create(
                    flight_number=f'DF204-{current_date.strftime("%Y%m%d")}',
                    flight_origin=self.airports['rotorua'],
                    flight_destination=self.airports['dairy_flat'],
                    flight_departure_time=make_datetime(current_date, 20, 0, self.airports['rotorua']),
                    flight_arrival_time=calculate_arrival_time(flight_departure_time, self.routes['rotorua'].route_duration_return, self.airports['dairy_flat']),
                    flight_aircraft=self.aircraft['cirrus1'],
                    fligh_price=self.routes['rotorua'].route_price
                )
                flights_created += 1
            
            #Add great barrier 
            for day_offset in range(5):  # Monday to Saturday
                current_date = week_start + timedelta(days=day_offset)
                
                # Monday, Wednesday, and Friday flights to Great Barrier Island
                # return flight on Tuesday, Thursday, and Saturday
                if day_offset % 2 == 0:  # Monday, Wednesday, and Friday
                    
                    flight_departure_time=make_datetime(current_date, 10, 0, self.airports['dairy_flat'])
                    
                    # Outbound flight to Great Barrier Island
                    Flight.objects.create(
                        flight_number=f'DF30{day_offset}-{current_date.strftime("%Y%m%d")}',
                        flight_origin=self.airports['dairy_flat'],
                        flight_destination=self.airports['great_barrier'],
                        flight_departure_time=make_datetime(current_date, 10, 0, self.airports['dairy_flat']),
                        flight_arrival_time=calculate_arrival_time(flight_departure_time, self.routes['great_barrier'].route_duration_return, self.airports['great_barrier']),
                        flight_aircraft=self.aircraft['cirrus2'],
                        fligh_price=self.routes['great_barrier'].route_price
                    )
                    flights_created += 1
                else:
                    flight_departure_time=make_datetime(current_date, 10, 0, self.airports['great_barrier'])
                    
                    # Return flight from Great Barrier Island
                    Flight.objects.create(
                        flight_number=f'DF30{day_offset}-{current_date.strftime("%Y%m%d")}',
                        flight_origin=self.airports['great_barrier'],
                        flight_destination=self.airports['dairy_flat'],
                        flight_departure_time=make_datetime(current_date, 10, 0, self.airports['great_barrier']),
                        flight_arrival_time=calculate_arrival_time(flight_departure_time, self.routes['great_barrier'].route_duration_return, self.airports['dairy_flat']),
                        flight_aircraft=self.aircraft['cirrus2'],
                        fligh_price=self.routes['great_barrier'].route_price
                    )
                    flights_created += 1
                    
            """
            A twice weekly service to Tuuta Airport in the Chatham Islands using one of the
            HondaJets. The outbound flights depart Dairy Flat on Tuesday and Friday, with the
            return flights departing Tuuta on Wednesday and Saturday.
            """
            
            for day_offset in range(5):
                current_date = week_start + timedelta(days=day_offset)
                
                # Tuesday and Friday flights to Chatham Islands
                if day_offset == 1 or day_offset == 4:
                    flight_departure_time=make_datetime(current_date, 10, 0, self.airports['dairy_flat'])
                    
                    # Outbound flight to Chatham Islands
                    Flight.objects.create(
                        flight_number=f'DF40{day_offset}-{current_date.strftime("%Y%m%d")}',
                        flight_origin=self.airports['dairy_flat'],
                        flight_destination=self.airports['chatham'],
                        flight_departure_time=make_datetime(current_date, 10, 0, self.airports['dairy_flat']),
                        flight_arrival_time=calculate_arrival_time(flight_departure_time, self.routes['chatham'].route_duration_return, self.airports['chatham']),
                        flight_aircraft=self.aircraft['hondajet1'],
                        fligh_price=self.routes['chatham'].route_price
                    )
                    flights_created += 1
                
                #Thursday and Saturday return flights from Chatham Islands
                if day_offset == 2 or day_offset == 5:
                    flight_departure_time=make_datetime(current_date, 10, 0, self.airports['chatham'])
                    
                    # Return flight from Chatham Islands
                    Flight.objects.create(
                        flight_number=f'DF40{day_offset}-{current_date.strftime("%Y%m%d")}',
                        flight_origin=self.airports['chatham'],
                        flight_destination=self.airports['dairy_flat'],
                        flight_departure_time=make_datetime(current_date, 10, 0, self.airports['chatham']),
                        flight_arrival_time=calculate_arrival_time(flight_departure_time, self.routes['chatham'].route_duration_return, self.airports['dairy_flat']),
                        flight_aircraft=self.aircraft['hondajet1'],
                        fligh_price=self.routes['chatham'].route_price
                    )
                    flights_created += 1
            """
                            Aweeklyservice to Lake Tekapo in the South Island using the other HondaJet. Departs
                        Dairy Flat on Monday with the return flight departing Tekapo on Tuesday.
 
            """

 
            for day_offset in range(5):
                    current_date = week_start + timedelta(days=day_offset)
                    
                    # Monday flights to Lake Tekapo
                    if day_offset == 0:
                        flight_departure_time=make_datetime(current_date, 10, 0, self.airports['dairy_flat'])
                        
                        # Outbound flight to Lake Tekapo
                        Flight.objects.create(
                            flight_number=f'DF50{day_offset}-{current_date.strftime("%Y%m%d")}',
                            flight_origin=self.airports['dairy_flat'],
                            flight_destination=self.airports['tekapo'],
                            flight_departure_time=make_datetime(current_date, 10, 0, self.airports['dairy_flat']),
                            flight_arrival_time=calculate_arrival_time(flight_departure_time, self.routes['tekapo'].route_duration_return, self.airports['tekapo']),
                            flight_aircraft=self.aircraft['hondajet2'],
                            fligh_price=self.routes['tekapo'].route_price
                        )
                        flights_created += 1
                    
                    # Tuesday return flights from Lake Tekapo
                    if day_offset == 1:
                        flight_departure_time=make_datetime(current_date, 10, 0, self.airports['tekapo'])
                        
                        # Return flight from Lake Tekapo
                        Flight.objects.create(
                            flight_number=f'DF50{day_offset}-{current_date.strftime("%Y%m%d")}',
                            flight_origin=self.airports['tekapo'],
                            flight_destination=self.airports['dairy_flat'],
                            flight_departure_time=make_datetime(current_date, 10, 0, self.airports['tekapo']),
                            flight_arrival_time=calculate_arrival_time(flight_departure_time, self.routes['tekapo'].route_duration_return, self.airports['dairy_flat']),
                            flight_aircraft=self.aircraft['hondajet2'],
                            fligh_price=self.routes['tekapo'].route_price
                        )
                        flights_created += 1
        self.stdout.write(f'Created {flights_created} flights')
            
        
        