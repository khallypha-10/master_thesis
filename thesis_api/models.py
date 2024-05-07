from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
# Create your models here.


class Doctor(models.Model):
    male = 'male'
    female = 'female'
    category_choices = [
        (male , 'male'), (female ,'female')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(null=True, blank=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    specialization = models.CharField(max_length=150)
    date_of_birth = models.DateField(auto_now=False, auto_now_add=False)
    language = models.CharField(max_length=50)
    gender = models.CharField(max_length=50, choices=category_choices)
    email = models.EmailField(max_length=254)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.user)
        super().save(*args, **kwargs)
    def __str__(self):
        return f"{self.first_name} || {self.last_name} || {self.specialization} || {self.email}"



class Patient(models.Model):
    male = 'male'
    female = 'female'
    category_choices = [
        (male , 'male'), (female ,'female')
    ]

    A_postive = 'A+'
    A_negative = 'A-'
    B_postive = 'B+'
    B_negative = 'B-'
    AB_postive = 'AB+'
    AB_negative = 'AB-'
    O_postive = 'O+'
    O_negative = 'O-'

    blood_type = [
        (A_postive , 'A+',),(A_negative , 'A-'),(B_postive , 'B+'),(B_negative , 'B-'),(AB_postive , 'AB+'),(AB_negative , 'AB-'),(O_postive , 'O+'),(O_negative , 'O-')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(null=True, blank=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField(auto_now=False, auto_now_add=False)
    language = models.CharField(max_length=50)
    gender = models.CharField(max_length=50, choices=category_choices)
    blood_type = models.CharField(max_length=50, choices=blood_type)
    email = models.EmailField(max_length=254)
    address = models.TextField()
    phone_number = models.IntegerField()
    allergies = models.TextField()    
    medical_conditions = models.TextField(help_text="write None if none ")
    current_medications = models.TextField(help_text="write None if none ")
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.user)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} || {self.last_name} || {self.blood_type} || {self.email} || {self.phone_number}"
    
class Prescriptions(models.Model):
    slug = models.SlugField(null=True, blank=True)
    medication = models.TextField(help_text="Please write the medication and dose.")
    prescribed_by = models.ForeignKey(Doctor, on_delete=models.SET_NULL, blank=True, null=True)
    prescribed_on = models.DateField(auto_now_add=True)   
    prescribe_for = models.ForeignKey("Patient", on_delete=models.SET_NULL, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.medication)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Prescriptions'
