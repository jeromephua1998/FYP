import os
import sys
import django

# Add the project directory to the sys.path
sys.path.append('/home/jerome/fyp/coursera/files/fyp')

# Set up the Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fyp.settings')
django.setup()

# Import your models here
from fypapp.models import Pet

def populate_pets():
    pets = [
        Pet(name="Buddy", age=2, breed="Golden Retriever", gender ="Male"),
        Pet(name="Tom", age=3, breed="Beagle", description="Loves to explore."),
        Pet(name="Whiskers", age=1, breed="Siamese Cat", description="Quiet and affectionate.", is_adopted=True)
    ]

    for pet in pets:
        pet.save()

if __name__ == "__main__":
    populate_pets()
    print("Pets have been populated.")
