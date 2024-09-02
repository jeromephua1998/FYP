from django.shortcuts import render, redirect
from .models import AppUser, Adopter, Shelter, Pet, Pet2, Event, Meeting
from .forms import PetFilterForm, CatFilterForm, RegistrationForm, ShelterRegistrationForm,PetRegistrationForm , CatRegistrationForm, EventForm, MeetingForm, ShelterProfileForm, AdopterProfileForm
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.contrib import messages


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('../login')


def dog_list(request):
    pets = Pet.objects.all().order_by('id')

    form = PetFilterForm(request.GET or None)

    if request.method == 'GET':

        name = request.GET.get('name')
        breed = request.GET.get('breed')
        gender = request.GET.get('gender')
        age = request.GET.get('age')

        if name:
            pets = pets.filter(name__startswith=name)
        if breed and breed != 'all':
            pets = pets.filter(breed__iexact=breed)
        if gender and gender != 'all':
            pets = pets.filter(gender__iexact=gender)
        if age and age != 'all':
            if age == 'puppy':
                pets = pets.filter(age__lte=1)
            elif age == 'adult':
                pets = pets.filter(age__gte=2, age__lte=8)
            elif age == 'senior':
                pets = pets.filter(age__gte=8)

    paginator = Paginator(pets, 12)

    page_number = request.GET.get('page')

    page_obj = paginator.get_page(page_number)

    return render(request, 'dog.html', {'page_obj': page_obj, 'form': form})


def cat_list(request):
    pets = Pet2.objects.all().order_by('id')

    form = CatFilterForm(request.GET or None)

    if request.method == 'GET':
        name = request.GET.get('name')
        breed = request.GET.get('breed')
        gender = request.GET.get('gender')
        age = request.GET.get('age')

        if name:
            pets = pets.filter(name__startswith=name)
        if breed and breed != 'all':
            pets = pets.filter(breed__iexact=breed)
        if gender and gender != 'all':
            pets = pets.filter(gender__iexact=gender)
        if age and age != 'all':
            if age == 'kitten':
                pets = pets.filter(age__lte=1)
            elif age == 'adult':
                pets = pets.filter(age__gte=2, age__lte=8)
            elif age == 'senior':
                pets = pets.filter(age__gte=8)

    paginator = Paginator(pets, 12)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'cat.html', {'page_obj': page_obj, 'form': form})



def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        form2 = ShelterRegistrationForm(request.POST)

        if form.is_valid() and 'adopter_register' in request.POST:
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            adopter = Adopter.objects.create(
                adopteremail=user.email,
                adopterFirstName=user.first_name,
                adopterLastName=user.last_name
            )

            AppUser.objects.create(user=user, usertype='adopter', adopterid=adopter)

            login(request, user)
            return redirect('home')

        elif form2.is_valid() and 'shelter_register' in request.POST:
            user = form2.save(commit=False)
            user.set_password(form2.cleaned_data['password'])
            user.save()

            sheltername = form2.cleaned_data['sheltername']
            contactnumber = form2.cleaned_data['contactnumber']

            shelter = Shelter.objects.create(
                sheltername=sheltername,
                email=user.email,
                contactnumber=contactnumber
            )

            AppUser.objects.create(user=user, usertype='shelter', shelterid=shelter)

            login(request, user)
            return redirect('home')

    else:
        form = RegistrationForm()
        form2 = ShelterRegistrationForm()

    return render(request, 'registration.html', {'form': form, 'form2': form2}) 

def user_login(request):
    if request.method == 'POST':
        if 'adopter_login' in request.POST:
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)

            if user is not None: 
                if user.is_active:
                    login(request, user)
                    return redirect('home')
                else:
                    messages.error(request, 'Account is inactive.')
            else:
                messages.error(request, 'Invalid login')

        elif 'shelter_login' in request.POST:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            
            if user is not None: 
                if user.is_active:
                    login(request, user)
                    return redirect('home')
                else:
                    messages.error(request, 'Account is inactive.')
            else:
                messages.error(request, 'Invalid login')

    return render(request, 'login.html')



def dogregister(request):
    user_profile = AppUser.objects.get(user=request.user)
    shelter = user_profile.shelterid
    if request.method == 'POST':
        form = PetRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            pet = form.save(commit=False)  
            pet.shelter = shelter  
            pet.save() 
            return redirect('dog_list')

    else:
        form = PetRegistrationForm()
    
    return render(request, 'dogregister.html', {'form': form})


def catregister(request):
    user_profile = AppUser.objects.get(user=request.user)
    shelter = user_profile.shelterid
    if request.method == 'POST':
        form = CatRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            pet = form.save(commit=False)  
            pet.shelter = shelter  
            pet.save()
            return redirect('cat_list') 
    else:
        form = CatRegistrationForm()
    
    return render(request, 'catregister.html', {'form': form})

def home(request):
    return render(request, 'home.html')


def petdesc(request, id):
    pet = get_object_or_404(Pet, id=id)
    return render(request, 'petdesc.html', {'pet': pet})


def catdesc(request, id):
    pet = get_object_or_404(Pet2, id=id)
    return render(request, 'catdesc.html', {'pet': pet})


def createevents(request):
    user_profile = AppUser.objects.get(user=request.user) 
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)

        if user_profile and user_profile.shelterid:
            shelter = user_profile.shelterid 
            event = form.save(commit=False)
            event.shelterid = shelter 
            event.save()
            return redirect('cat_list')  
    else:
        form = EventForm()

    return render(request, 'createvents.html', {'form': form})




def view_events(request):

    user_profile = AppUser.objects.get(user=request.user)
    
    if user_profile.shelterid:
   
        events = Event.objects.filter(shelterid=user_profile.shelterid)
    elif user_profile.adopterid:
        events = Event.objects.all()

    return render(request, 'viewevents.html', {'events': events})




def eventsview(request, eventid):
    event = get_object_or_404(Event, pk=eventid)

    return render(request, 'events.html', {'event': event})


def editevent(request, eventid):
    event = get_object_or_404(Event, pk=eventid)
    
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            return redirect('view_events')  
    else:
        form = EventForm(instance=event)  
    
    return render(request, 'editevents.html', {'form': form, 'event': event})


def deleteevents(request, eventid):
    event = get_object_or_404(Event, pk=eventid)
    event.delete()
    return redirect('view_events')  


def createmeeting(request, pet_id):
    pet = get_object_or_404(Pet, pk=pet_id)
    
    if request.method == 'POST':
        form = MeetingForm(request.POST)
        if form.is_valid():
            meeting = form.save(commit=False)
            meeting.pet = pet  
            meeting.save()
            return redirect('home')  
        else:
            print(form.errors)
    else:
        form = MeetingForm()
    
    return render(request, 'adoption.html', {'form': form, 'pet': pet})


def viewmeeting(request):

    user_profile = request.user.appuser  
    shelter_id = user_profile.shelterid_id
    shelter_pets = Pet.objects.filter(shelter_id=shelter_id)
    meetings = Meeting.objects.filter(pet__in=shelter_pets)

    return render(request, 'viewmeeting.html', {'meetings': meetings})


def editprofile(request):
    user_profile = get_object_or_404(AppUser, user=request.user)
    
    if user_profile.usertype == 'adopter':
        if request.method == 'POST':
            form = AdopterProfileForm(request.POST, instance=user_profile.adopterid)
            if form.is_valid():
                form.save()
                return redirect('home') 
        else:
            form = AdopterProfileForm(instance=user_profile.adopterid)
    
    elif user_profile.usertype == 'shelter':
        if request.method == 'POST':
            form = ShelterProfileForm(request.POST, instance=user_profile.shelterid)
            if form.is_valid():
                form.save()
                return redirect('home')
        else:
            form = ShelterProfileForm(instance=user_profile.shelterid)
    
    return render(request, 'profile.html', {'form': form})


def donation(request):
    return render(request, 'donation.html')

def faqview(request):
    return render(request, 'faq.html')
