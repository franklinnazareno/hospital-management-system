from django.contrib.auth.models import User
from django.db import models

# Create your models here.
SEX = [
    ('Male', 'Male'),
    ('Female', 'Female'),
]

# DEPARTMENT_CHOICES = [
#     ('Allied Medical Specialties', 'DEPARTMENT OF ALLIED MEDICAL SPECIALTIES'),
#     ('Cardiology', 'DEPARTMENT OF CARDIOLOGY'),
#     ('Cardiovascular Surgery Anesthesia', 'DEPARTMENT OF CARDIOVASCULAR SURGERY and ANESTHESIA'),
#     ('Education Training Research', 'DEPARTMENT OF EDUCATION, TRAINING and RESEARCH'),
#     ('Pediatric Cardiology', 'DEPARTMENT OF PEDIATRIC CARDIOLOGY'),
#     ('Ambulatory Emergency Care', 'DEPARTMENT OF AMBULATORY and EMERGENCY CARE'),
# ]

class Doctor(models.Model):
    user = models.OneToOneField(User, null=False, blank=False, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='doctor_profile_pics', null=False, blank=False)
    department_id = models.PositiveIntegerField(null=True)
    sex = models.CharField(max_length=10, blank=False, null=False, choices=SEX)
    status = models.BooleanField(default=False, blank=False, null=False)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return "Dr. {} {}".format(self.user.first_name, self.user.last_name)

class Department(models.Model):
    department_name = models.CharField(max_length=100, blank=False, null=False)
    doctor_id = models.PositiveIntegerField(null=True, blank=True)
    def __str__(self):
        return self.department_name

class Patient(models.Model):
    user = models.OneToOneField(User, blank=False, null=False, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='patient_profile_pics', null=False, blank=False)    
    sex = models.CharField(max_length=10, blank=False, null=False, choices=SEX)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return self.user.last_name+", "+self.user.first_name

class Appointment(models.Model):
    patient_id = models.PositiveIntegerField(null=True)
    doctor_id = models.PositiveIntegerField(null=True)
    appointment_date = models.DateField(auto_now_add=False, auto_now=False, blank=False, null=False)
    appointment_time = models.TimeField(auto_now_add=False, auto_now=False, blank=False, null=False)
    appointment_reason = models.TextField(max_length=255)
    appointment_status = models.BooleanField(default=False)
    appointment_comments = models.TextField(max_length=255, blank=True, null=True)
    def __str__(self):
        return self.patient_name+" "+str(self.appointment_date)+" "+str(self.appointment_time)