from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .models import *
import re
from django.core.exceptions import ValidationError
from django.utils import timezone



class PetFilterForm(forms.Form):
    name = forms.CharField(max_length=100, required=False)
    breed = forms.ChoiceField(
        choices=[
            ('all', 'All'),
            ('golden retriever', 'Golden Retriever'),
            ('labrador retriever', 'Labrador Retriever'),
            ('german shepherd', 'German Shepherd'),
            ('bulldog', 'Bulldog'),
            ('poodle', 'Poodle'),
            ('affenpinscher', 'Affenpinscher'),
            ('australian silky terrier', 'Australian Silky Terrier'),
            ('australian terrier', 'Australian Terrier'),
            ('bichon avanese', 'Bichon Avanese'),
            ('bichon frise', 'Bichon Frise'),
            ('bohemian terrier', 'Bohemian Terrier'),
            ('bolognese', 'Bolognese'),
            ('border terrier', 'Border Terrier'),
            ('boston terrier', 'Boston Terrier'),
            ('brussels griffon', 'Brussels Griffon'),
            ('cairn terrier', 'Cairn Terrier'),
            ('cavalier king charles spaniel', 'Cavalier King Charles Spaniel'),
            ('chihuahua', 'Chihuahua'),
            ('chinese crested dog', 'Chinese Crested Dog'),
            ('chinese imperial chin', 'Chinese Imperial Chin'),
            ('chinese temple dog', 'Chinese Temple Dog'),
            ('coton de tulear', 'Coton de Tulear'),
            ('czech terrier', 'Czech Terrier'),
            ('dachshund', 'Dachshund'),
            ('dandie dinmont terrier', 'Dandie Dinmont Terrier'),
            ('english toy spaniel', 'English Toy Spaniel'),
            ('german hunting terrier', 'German Hunting Terrier'),
            ('griffon belge', 'Griffon Belge'),
            ('griffon brabancon', 'Griffon Brabancon'),
            ('hairless dog', 'Hairless Dog'),
            ('italian greyhound', 'Italian Greyhound'),
            ('jack russell terrier', 'Jack Russell Terrier'),
            ('japanese spaniel chin', 'Japanese Spaniel (Chin)'),
            ('japanese spitz', 'Japanese Spitz'),
            ('lakeland terrier', 'Lakeland Terrier'),
            ('lhasa apso', 'Lhasa Apso'),
            ('little lion dog', 'Little Lion Dog'),
            ('maltese', 'Maltese'),
            ('manchester terrier', 'Manchester Terrier'),
            ('miniature pinscher', 'Miniature Pinscher'),
            ('miniature schnauzer', 'Miniature Schnauzer'),
            ('norfolk terrier', 'Norfolk Terrier'),
            ('norwegian lundehund', 'Norwegian Lundehund'),
            ('norwich terrier', 'Norwich Terrier'),
            ('papillon', 'Papillon'),
            ('pekingnese', 'Pekingnese'),
            ('pomeranian', 'Pomeranian'),
            ('poodle toy miniature', 'Poodle (Toy / Miniature)'),
            ('pug', 'Pug'),
            ('schipperkee', 'Schipperkee'),
            ('scottish terrier', 'Scottish Terrier'),
            ('sealyham terrier', 'Sealyham Terrier'),
            ('shetland sheepdog', 'Shetland Sheepdog'),
            ('shih tzu', 'Shih Tzu'),
            ('silky terrier', 'Silky Terrier'),
            ('small continental spaniel', 'Small Continental Spaniel'),
            ('small english terrier', 'Small English Terrier'),
            ('small spitz', 'Small Spitz'),
            ('smooth fox terrier', 'Smooth Fox Terrier'),
            ('tibetan spaniel', 'Tibetan Spaniel'),
            ('toy fox terrier', 'Toy Fox Terrier'),
            ('toy terrier', 'Toy Terrier'),
            ('volpino italiano', 'Volpino Italiano'),
            ('welsh terrier', 'Welsh Terrier'),
            ('west highland terrier', 'West Highland Terrier'),
            ('wire haired fox terrier', 'Wire-Haired Fox Terrier'),
            ('yorkshire terrier', 'Yorkshire Terrier'),
        ],
        required=False
    )

    gender = forms.ChoiceField(choices=[('all', 'All'), ('male', 'Male'), ('female', 'Female')], required=False)
    age = forms.ChoiceField(choices=[('all', 'All'), ('puppy', 'Puppy'), ('adult', 'Adult'),('senior', 'Senior')], required=False)


class CatFilterForm(forms.Form):
    name = forms.CharField(max_length=100, required=False)
    breed = forms.ChoiceField(choices=[
        ('all', 'All'),('persian', 'Persian'),
        ('maine coon', 'Maine Coon'),
        ('ragdoll', 'Ragdoll'),
        ('british shorthair', 'British Shorthair'),
        ('siamese', 'Siamese'),
        ('sphynx', 'Sphynx'),
        ('bengal', 'Bengal'),
        ('scottish fold', 'Scottish Fold'),
        ('siberian', 'Siberian'),
        ('abyssinian', 'Abyssinian'),], required=False)
    gender = forms.ChoiceField(choices=[('all', 'All'), ('male', 'Male'), ('female', 'Female')], required=False)
    age = forms.ChoiceField(choices=[('all', 'All'), ('kitten', 'Kitten'), ('adult', 'Adult'),('senior', 'Senior')], required=False)


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name')
        help_texts = {
            'username': None,
        }

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username is already in use.")

        if len(username) < 4:
            raise forms.ValidationError("Username cannot be shorter than 4 characters.")
        if len(username) > 20:
            raise forms.ValidationError("Username cannot be longer than 20 characters.")
        return username

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 6:
            raise forms.ValidationError("Password cannot be shorter than 6 characters")
        if len(password) > 20:
            raise forms.ValidationError("Password cannot be longer than 20 characters.")

        if not re.search('[A-Z]', password):
            raise ValidationError("Password must contain at least one uppercase letter.")

        if not re.search('[0-9]', password):
            raise ValidationError("Password must contain at least one digit.")

        if not re.search('[^A-Za-z0-9]', password):
            raise ValidationError("Password must contain at least one special character.")

        return password 

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email is already in use.")
        return email
    

    def clean_firstname(self):
         first_name = self.cleaned_data.get('adopterFirstName')
         if not first_name.isalpha():
            raise forms.ValidationError("First name only should contain alphabets")
         if len(first_name) < 2 or len(first_name) > 40:
            raise forms.ValidationError("First name must be between 2 characters and 40")
         return first_name
         
    def clean_lastname(self):
         last_name = self.cleaned_data.get('adopterLastName')
         if not last_name.isalpha():
            raise forms.ValidationError("Last name only should contain alphabets")
         if len(last_name) < 2 or len(last_name) > 40:
            raise forms.ValidationError("Last name must be between 2 characters and 40")
         return last_name


    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = make_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
    
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.required = True

    

class ShelterRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    sheltername = forms.CharField(max_length=100)
    contactnumber = forms.CharField(max_length=15)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) < 4 or len(username) > 20:
            raise forms.ValidationError("Username must be between 4 and 20 characters long.")
        return username

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 6 or len(password) > 20:
            raise forms.ValidationError("Password must be between 6 and 20 characters long.")
        return password

    def clean_sheltername(self):
        sheltername = self.cleaned_data.get('sheltername')
        if len(sheltername) < 5 or len(sheltername) > 30:
            raise forms.ValidationError("Shelter name must be between 5 and 30 characters long.")
        return sheltername

    def clean_contactnumber(self):
        contactnumber = self.cleaned_data.get('contactnumber')
        regex = re.compile(r"^[689][0-9]{7}$")
        if not regex.match(contactnumber):
            raise forms.ValidationError("Number must be a valid Singapore number")
        contactnumber = "+65" + contactnumber
        return contactnumber

    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = make_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = AppUser
        fields = ('usertype',)


class ProfileForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password')

class PetRegistrationForm(forms.ModelForm):
    BREED_CHOICES = [
('golden retriever', 'Golden Retriever'),
('labrador retriever', 'Labrador Retriever'),
('german shepherd', 'German Shepherd'),
('bulldog', 'Bulldog'),
('poodle', 'Poodle'),
('affenpinscher', 'Affenpinscher'),
('australian silky terrier', 'Australian Silky Terrier'),
('australian terrier', 'Australian Terrier'),
('bichon avanese', 'Bichon Avanese'),
('bichon frise', 'Bichon Frise'),
('bohemian terrier', 'Bohemian Terrier'),
('bolognese', 'Bolognese'),
('border terrier', 'Border Terrier'),
('boston terrier', 'Boston Terrier'),
('brussels griffon', 'Brussels Griffon'),
('cairn terrier', 'Cairn Terrier'),
('cavalier king charles spaniel', 'Cavalier King Charles Spaniel'),
('chihuahua', 'Chihuahua'),
('chinese crested dog', 'Chinese Crested Dog'),
('chinese imperial chin', 'Chinese Imperial Chin'),
('chinese temple dog', 'Chinese Temple Dog'),
('coton de tulear', 'Coton de Tulear'),
('czech terrier', 'Czech Terrier'),
('dachshund', 'Dachshund'),
('dandie dinmont terrier', 'Dandie Dinmont Terrier'),
('english toy spaniel', 'English Toy Spaniel'),
('german hunting terrier', 'German Hunting Terrier'),
('griffon belge', 'Griffon Belge'),
('griffon brabancon', 'Griffon Brabancon'),
('hairless dog', 'Hairless Dog'),
('italian greyhound', 'Italian Greyhound'),
('jack russell terrier', 'Jack Russell Terrier'),
('japanese spaniel chin', 'Japanese Spaniel (Chin)'),
('japanese spitz', 'Japanese Spitz'),
('lakeland terrier', 'Lakeland Terrier'),
('lhasa apso', 'Lhasa Apso'),
('little lion dog', 'Little Lion Dog'),
('maltese', 'Maltese'),
('manchester terrier', 'Manchester Terrier'),
('miniature pinscher', 'Miniature Pinscher'),
('miniature schnauzer', 'Miniature Schnauzer'),
('norfolk terrier', 'Norfolk Terrier'),
('norwegian lundehund', 'Norwegian Lundehund'),
('norwich terrier', 'Norwich Terrier'),
('papillon', 'Papillon'),
('pekingnese', 'Pekingnese'),
('pomeranian', 'Pomeranian'),
('poodle toy miniature', 'Poodle (Toy / Miniature)'),
('pug', 'Pug'),
('schipperkee', 'Schipperkee'),
('scottish terrier', 'Scottish Terrier'),
('sealyham terrier', 'Sealyham Terrier'),
('shetland sheepdog', 'Shetland Sheepdog'),
('shih tzu', 'Shih Tzu'),
('silky terrier', 'Silky Terrier'),
('small continental spaniel', 'Small Continental Spaniel'),
('small english terrier', 'Small English Terrier'),
('small spitz', 'Small Spitz'),
('smooth fox terrier', 'Smooth Fox Terrier'),
('tibetan spaniel', 'Tibetan Spaniel'),
('toy fox terrier', 'Toy Fox Terrier'),
('toy terrier', 'Toy Terrier'),
('volpino italiano', 'Volpino Italiano'),
('welsh terrier', 'Welsh Terrier'),
('west highland terrier', 'West Highland Terrier'),
('wire haired fox terrier', 'Wire-Haired Fox Terrier'),
('yorkshire terrier', 'Yorkshire Terrier')
]

    SIZE_CHOICES = [
        ('small', 'Small'),
        ('medium', 'Medium'),
        ('large', 'Large'),
    ]

    COLOR_CHOICES = [
        ('brown', 'Brown'),
        ('beige', 'Beige'),
        ('golden', 'Golden'),
        ('white', 'White'),
        ('black', 'Black'),
    ]

    breed = forms.ChoiceField(choices=BREED_CHOICES)
    size = forms.ChoiceField(choices=SIZE_CHOICES)
    color = forms.ChoiceField(choices=COLOR_CHOICES)

    class Meta:
        model = Pet
        fields = ['name', 'breed', 'age', 'gender', 'size', 'color', 'description', 'likes', 'image']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name) > 40:
            raise forms.ValidationError("Name must be 40 characters")
        return name

    def clean_description(self):
        description = self.cleaned_data.get('description')
        word_count = len(description.split())
        if word_count < 50 or word_count > 300:
            raise forms.ValidationError("Description must be between 50 and 300 words.")
        return description

    def clean_likes(self):
        likes = self.cleaned_data.get('likes')
        word_count = len(likes.split())
        if word_count < 20 or word_count > 100:
            raise forms.ValidationError("Likes must be between 20 and 100 words.")
        return likes

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age >= 35:
            raise forms.ValidationError("Age must be less than 35 years.")
        return age

class CatRegistrationForm(forms.ModelForm):
    BREED_CHOICES = [
        ('persian', 'Persian'),
        ('maine coon', 'Maine Coon'),
        ('ragdoll', 'Ragdoll'),
        ('british shorthair', 'British Shorthair'),
        ('siamese', 'Siamese'),
        ('sphynx', 'Sphynx'),
        ('bengal', 'Bengal'),
        ('scottish fold', 'Scottish Fold'),
        ('siberian', 'Siberian'),
        ('abyssinian', 'Abyssinian'),
    ]

    SIZE_CHOICES = [
        ('small', 'Small'),
        ('medium', 'Medium'),
        ('large', 'Large'),
    ]

    COLOR_CHOICES = [
        ('brown', 'Brown'),
        ('white', 'White'),
        ('black', 'Black'),
        ('gray', 'Gray'),
        ('orange', 'Orange'),
        ('cream', 'Cream'),
        ('blue', 'Blue'),
        ('calico', 'Calico'),
        ('tabby', 'Tabby'),
    ]
    breed = forms.ChoiceField(choices=BREED_CHOICES)
    size = forms.ChoiceField(choices=SIZE_CHOICES)
    color = forms.ChoiceField(choices=COLOR_CHOICES)

    class Meta:
        model = Pet2
        fields = ['name', 'breed', 'age', 'gender', 'size', 'color', 'description', 'likes', 'image']


    def clean_likes(self):
        likes = self.cleaned_data.get('likes')
        word_count = len(likes.split())
        if word_count < 20 or word_count > 100:
            raise forms.ValidationError("Likes must be between 20 and 100 words.")
        return likes


    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name) > 40:
            raise forms.ValidationError("Name must be 40 characters or fewer.")
        return name

    def clean_description(self):
        description = self.cleaned_data.get('description')
        word_count = len(description.split())
        if word_count < 50 or word_count > 300:
            raise forms.ValidationError("Description must be between 50 and 300 words.")
        return description

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age >= 35:
            raise forms.ValidationError("Age must be less than 35 years.")
        return age


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'startdate', 'enddate', 'location', 'image']
        widgets = {
            'startdate': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'enddate': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 5 or len(title) > 40:
            raise ValidationError("Title must be between 5 and 40 characters.")
        return title

    def clean_description(self):
        description = self.cleaned_data.get('description')
        word_count = len(description.split())
        if word_count < 50 or word_count > 1000:
            raise ValidationError("Description must be between 50 and 1000 words.")
        return description

    def clean_startdate(self):
        startdate = self.cleaned_data.get('startdate')
        if startdate <= timezone.now():
            raise ValidationError("Start date must be later than the current date and time.")
        return startdate

    def clean_enddate(self):
        enddate = self.cleaned_data.get('enddate')
        startdate = self.cleaned_data.get('startdate')

        if startdate and enddate and enddate < startdate:
            raise ValidationError("End date must be later than the start date.")
        return enddate




class MeetingForm(forms.ModelForm):
    class Meta:
        model = Meeting
        fields = ['fullname', 'phonenumber', 'address', 'email', 'about', 'experience', 'meeting_time']
        widgets = {
            'meeting_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'experience': forms.Select(choices=[('yes', 'Yes'), ('no', 'No')])
        }

    def clean_fullname(self):
        fullname = self.cleaned_data.get('fullname')
        if len(fullname) > 40:
            raise ValidationError("Full name must be 40 characters or less.")
        return fullname

    def clean_phonenumber(self):
        phonenumber = self.cleaned_data.get('phonenumber')
        regex = re.compile(r"^[689][0-9]{7}$")
        if not regex.match(phonenumber):
            raise ValidationError("Number must be a valid Singapore number.")
        phonenumber = "+65" + phonenumber
        return phonenumber

    def clean_email(self):
        email = self.cleaned_data.get('email')
        return email

    def clean_about(self):
        about = self.cleaned_data.get('about')
        word_count = len(about.split())
        if word_count < 50 or word_count > 200: 
            raise ValidationError("About must be between 50 to 200 words.")
        return about

    def clean_meeting_time(self):
        meeting_time = self.cleaned_data.get('meeting_time')
        if meeting_time and meeting_time <= timezone.now():
            raise ValidationError("Meeting time must be in the future.")
        return meeting_time
    
    def clean_address(self):
        address = self.cleaned_data.get('address')
        if len(address) < 10:
            raise ValidationError("Address must be at least 10 characters long.")
        return address
    

class AdopterProfileForm(forms.ModelForm):
    class Meta:
        model = Adopter
        fields = ['adopterFirstName', 'adopterLastName', 'adopteremail']

    def clean_firstname(self):
        first_name = self.cleaned_data.get('adopterFirstName')
        if not first_name.isalpha():
            raise forms.ValidationError("First name must only contain alphabetic characters.")
        if len(first_name) < 2 or len(first_name) > 40:
            raise forms.ValidationError("First name must be between 2 and 40 characters long.")
        return first_name

    def clean_lastname(self):
        last_name = self.cleaned_data.get('adopterLastName')
        if not last_name.isalpha():
            raise forms.ValidationError("Last name must only contain alphabetic characters.")
        if len(last_name) < 2 or len(last_name) > 40:
            raise forms.ValidationError("Last name must be between 2 and 40 characters long.")
        return last_name
    
    def clean_email(self):
        email = self.cleaned_data['adopteremail']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email is already in use.")
        return email


class ShelterProfileForm(forms.ModelForm):
    class Meta:
        model = Shelter
        fields = ['sheltername', 'email', 'contactnumber']
        
    def clean_sheltername(self):
        sheltername = self.cleaned_data.get('sheltername')
        if len(sheltername) < 5 or len(sheltername) > 30:
            raise forms.ValidationError("Shelter name must be between 5 and 30 characters long.")
        return sheltername


    def clean_phonenumber(self):
        phonenumber = self.cleaned_data.get('contactnumber')
        regex = re.compile(r"^[689][0-9]{7}$")
        if not regex.match(phonenumber):
            raise ValidationError("Number must be a valid Singapore number.")
        phonenumber = "+65" + phonenumber
        return phonenumber
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email is already in use.")
        return email

