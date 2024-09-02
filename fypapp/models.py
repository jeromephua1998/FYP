from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User

class Adopter(models.Model):
    adopterid = models.AutoField(primary_key=True)
    adopteremail = models.EmailField(unique=True)
    adopterFirstName = models.CharField(max_length=100,default='John')
    adopterLastName = models.CharField(max_length=100,default='Doe')

    def __str__(self):
        return self.adopteremail


class Shelter(models.Model):
    shelterid = models.AutoField(primary_key=True)
    sheltername = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    contactnumber = models.CharField(max_length=15)

    def __str__(self):
        return self.sheltername
    

class AppUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    USERTYPES = (
        ('adopter', 'Adopter'),
        ('shelter', 'Shelter'),
    )
    usertype = models.CharField(max_length=10, choices=USERTYPES)
    shelterid = models.ForeignKey(Shelter, on_delete=models.CASCADE, null=True, blank=True)
    adopterid = models.ForeignKey(Adopter, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.user.username

class Pet(models.Model):
    name = models.CharField(max_length=100, null=True)
    breed = models.CharField(max_length=100, null=True)
    age = models.PositiveIntegerField(null=True)
    size = models.CharField(max_length=50, null=True)
    color = models.CharField(max_length=50, null=True)  
    description = models.TextField(null=True)
    likes = models.TextField(null=True)
    image = models.ImageField(upload_to='pet_images/', null=True)
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female')])
    shelter = models.ForeignKey(Shelter, on_delete=models.SET_NULL, null=True, blank=True, related_name='pets')

    def __str__(self):
        return self.name
    

class Pet2(models.Model):
        name = models.CharField(max_length=100, null=True)
        breed = models.CharField(max_length=100, null=True)
        age = models.PositiveIntegerField(null=True)
        size = models.CharField(max_length=50, null=True)
        color = models.CharField(max_length=50, null=True)  
        description = models.TextField(null=True)
        likes = models.TextField(null=True)
        image = models.ImageField(upload_to='pet_images/', null=True)
        gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female')])
        shelter = models.ForeignKey(Shelter, on_delete=models.SET_NULL, null=True, blank=True, related_name='pets2')

        def __str__(self):
            return self.name


class Event(models.Model):
    eventid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    startdate = models.DateTimeField(null=True) 
    enddate = models.DateTimeField(null=True)    
    location = models.CharField(max_length=255)
    image = models.ImageField(upload_to='event_images/', null=True, blank=True)
    shelterid = models.ForeignKey(Shelter, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    


class Meeting(models.Model):
    meetingid = models.AutoField(primary_key=True)
    fullname = models.CharField(max_length=255)
    phonenumber = models.CharField(max_length=20) 
    address = models.TextField(null=True, blank=True) 
    email = models.EmailField()  
    about = models.TextField() 
    experience = models.CharField(max_length=255) 
    meeting_time = models.DateTimeField() 
    pet = models.ForeignKey('Pet', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"Meeting with {self.fullname} at {self.meeting_time}"