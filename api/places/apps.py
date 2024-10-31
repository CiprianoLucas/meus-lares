from django.apps import AppConfig
from django.conf import settings
from django.db.models.signals import post_migrate
from django.utils.module_loading import import_string
import json
import os

class PlacesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'places'
    verbose_name = "lugares"

    def ready(self):
        post_migrate.connect(create_states_and_cities, sender=self)
    
def create_states_and_cities(sender, **kwargs):

    State = import_string("places.models.State")
    City = import_string("places.models.City")

    if not State.objects.exists():
        print("Created States and Cities")
        states_path = os.path.join(settings.BASE_DIR, "places", "assets", "states.json")
        cities_path = os.path.join(settings.BASE_DIR, "places", "assets", "cities.json")
        
        with open(states_path, encoding='utf-8') as f:
            states = json.load(f)
            
        with open(cities_path, encoding='utf-8') as f:
            cities = json.load(f)
            
        states_objs = [State(name=state['name'], acronym=state['acronym']) for state in states] 
           
        State.objects.bulk_create(states_objs)
        
        state_id_map = {state.acronym: state for state in State.objects.all()}
        
        cities_objs = [City(name=city['name'], state=state_id_map[city['state']]) for city in cities]
        
        City.objects.bulk_create(cities_objs)