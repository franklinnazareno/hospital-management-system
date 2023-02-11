from django import forms
from datetimepicker.widgets import DateTimePicker
from django.contrib.auth.models import User
from django.views.generic.edit import UpdateView
from . import models
from django.contrib.auth.forms import UserChangeForm

class AdminUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {'password':forms.PasswordInput()}

class DoctorUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password']
        widgets = {'password':forms.PasswordInput()}

class EditDoctorUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email',]

class DoctorForm(forms.ModelForm):
    department_id = forms.ModelChoiceField(queryset=models.Department.objects.all(), empty_label="Choose your Department", to_field_name="id", label="Department")
    class Meta:
        model = models.Doctor
        fields = ['sex', 'profile_pic']

class EditDoctorForm(forms.ModelForm):
    department_id = forms.ModelChoiceField(queryset=models.Department.objects.all(), empty_label="Choose your Department", to_field_name="id", label="Department")
    class Meta:
        model = models.Doctor
        fields = ['sex', 'profile_pic',]

class AdminEditDoctorForm(forms.ModelForm):
    department_id = forms.ModelChoiceField(queryset=models.Department.objects.all(), empty_label="Choose your Department", to_field_name="id", label="Department")
    class Meta:
        model = models.Doctor
        fields = ['status',]

class PatientUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password']
        widgets = {'password':forms.PasswordInput()}

class EditPatientUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email',]

class PatientForm(forms.ModelForm):
    # chosen_doctor_id = forms.ModelChoiceField(queryset=models.Doctor.objects.all().filter(status=True), empty_label="Name and Department", to_field_name="user_id")
    class Meta:
        model = models.Patient
        fields = ['sex', 'profile_pic']

class EditPatientForm(forms.ModelForm):
    # chosen_doctor_id = forms.ModelChoiceField(queryset=models.Doctor.objects.all().filter(status=True), empty_label="Name and Department", to_field_name="user_id")
    class Meta:
        model = models.Patient
        fields = ['sex', 'profile_pic']

class ChangePatientProfilePic(forms.ModelForm):
        class Meta:
            model = models.Patient
            fields = ['profile_pic',]

class PatientAppointmentForm(forms.ModelForm):
    doctor_id = forms.ModelChoiceField(queryset=models.Doctor.objects.all().filter(status=True), empty_label="Choose your Doctor", to_field_name="user_id", label="Doctor")
    class Meta:
        model = models.Appointment
        fields = ['appointment_date', 'appointment_time', 'appointment_reason',]

class PatientEditAppointmentForm(forms.ModelForm):
    doctor_id = forms.ModelChoiceField(queryset=models.Doctor.objects.all().filter(status=True), empty_label="Choose your Doctor", to_field_name="user_id", label="Doctor")
    class Meta:
        model = models.Appointment
        fields = ['appointment_date', 'appointment_time', 'appointment_reason',]

class DoctorEditAppointmentForm(forms.ModelForm):
    class Meta:
        model = models.Appointment
        fields = ['appointment_status', 'appointment_comments',]

class DepartmentForm(forms.ModelForm):
    doctor_id = forms.ModelChoiceField(queryset=models.Doctor.objects.all().filter(status=True), empty_label="Choose your Doctor", to_field_name="user_id", label="Doctor", required=False)
    class Meta:
        model = models.Department
        fields = ['department_name',]

class EditDepartmentForm(forms.ModelForm):
    doctor_id = forms.ModelChoiceField(queryset=models.Doctor.objects.all().filter(status=True), empty_label="Choose your Doctor", to_field_name="user_id", label="Doctor", required=False)
    class Meta:
        model = models.Department
        fields = ['department_name',]