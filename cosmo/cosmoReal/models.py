from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

class Filter(models.Model):
    WORK_CHOICE = (
    ('commercial','Commercial'),
    ('residential', 'Residential'),
    )
    TYPE_CHOICE = (
    ('apartment','Apartment'),
    ('villa', 'Villa'),
    )
    CITY_CHOICE = (
    ('mumbai','Mumbai'),
    ('chennai', 'Chennai'),
    ('bengaluru','Bengaluru'),
    ('hyderabad', 'Hyderabad'),
    )

    proptype = models.CharField(max_length=50,choices=TYPE_CHOICE,blank=True,null=True)
    #price = models.IntegerField()
    city = models.CharField(max_length=50,choices=CITY_CHOICE,blank=True,null=True)
    use = models.CharField(max_length=50, choices=WORK_CHOICE,blank=True,null=True)
   
class Buy(models.Model):
    WORK_CHOICE = (
    ('commercial','Commercial'),
    ('residential', 'Residential'),
    )

    propid = models.CharField(max_length=200)
    proptype = models.CharField(max_length=50)
    price = models.IntegerField()
    description = models.TextField(default='')
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    use = models.CharField(max_length=50, choices=WORK_CHOICE)
    image1 = models.ImageField(upload_to ='uploads/')
    image2 = models.ImageField(upload_to ='uploads/')
    image3 = models.ImageField(upload_to ='uploads/')
    posted_date = models.DateTimeField(default=timezone.now)

    def publish(self):
        self.posted_date = timezone.now()
        self.save()

    def __str__(self):
        return self.propid

class Sell(models.Model):
    seller = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    image0 = models.ImageField(upload_to ='userimages/')
    image1 = models.ImageField(upload_to ='userimages/')
    image2 = models.ImageField(upload_to ='userimages/')
    posted_date = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return self.seller

class Rent(models.Model):
    WORK_CHOICE = (
    ('commercial','Commercial'),
    ('residential', 'Residential'),
    )
    propid = models.CharField(max_length=200)
    proptype = models.CharField(max_length=50)
    price = models.IntegerField()
    description = models.TextField(default='')
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    use = models.CharField(max_length=50, choices=WORK_CHOICE)
    image1 = models.ImageField(upload_to ='uploads/')
    image2 = models.ImageField(upload_to ='uploads/')
    image3 = models.ImageField(upload_to ='uploads/')
    posted_date = models.DateTimeField(default=timezone.now)

    def publish(self):
        self.posted_date = timezone.now()
        self.save()

    def __str__(self):
        return self.propid

class Tenant(models.Model):
    MAINTENANCE_CHOICES = (
    ('home cleaning','Home Cleaning'),
    ('pest control', 'Pest Control'),
    ('sanitization','Sanitization'),
    ('plumbing','Plumbing'),
    ('other','Other'),
    )
    name = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    propertyid = models.CharField(max_length=200)
    address = models.TextField()
    due = models.IntegerField()
    issues = models.CharField(max_length=50,choices=MAINTENANCE_CHOICES,null=True,blank=True,default='')
    request = models.CharField(max_length=50,null=True,blank=True,default='None')
    email = models.EmailField(max_length=100)
    posted_date = models.DateTimeField(default=timezone.now)

    def publish(self):
        self.posted_date = timezone.now()
        self.save()
  
    def __str__(self):
        return self.propertyid

class Appointment(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=100)
    date = models.DateField()
    posted_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name
    


