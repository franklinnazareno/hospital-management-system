from django.shortcuts import render, reverse
from django.urls import reverse_lazy 
from django.contrib.auth import authenticate, login, logout as django_logout
from . import forms, models
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView

is_patient = False
is_doctor = False
doctor_status = False

class PasswordsChangeView(PasswordChangeView):
    form_class = PasswordChangeForm
    template_name='hms_app/change_password.html'
    success_url = reverse_lazy('hms_app:password_changed')

    def get_context_data(self, **kwargs):
        global is_patient
        global is_doctor
        global doctor_status
        context = super().get_context_data(**kwargs)
        context['is_patient'] = is_patient
        context['is_doctor'] = is_doctor
        context['doctor_status'] = doctor_status
        return context

@login_required
def password_changed(request):
    global is_patient
    global is_doctor
    global doctor_status
    context = {'is_patient':is_patient, 'is_doctor':is_doctor, 'doctor_status':doctor_status}
    return render(request, 'hms_app/change_password_success.html', context)

def index(request):
    global is_patient
    global is_doctor
    global doctor_status
    if is_patient:
        patient = models.Patient.objects.get(user_id=request.user.id)
        doctor_list = models.Doctor.objects.all().filter(status=True)
        appointment_list = models.Appointment.objects.all().filter(patient_id=patient.id)
        return render(request, 'hms_app/index.html', {'is_patient':is_patient, 'is_doctor':is_doctor, 'appointment_list': appointment_list, 'doctor_list': doctor_list})
    elif is_doctor:
        doctor = models.Doctor.objects.get(user_id=request.user.id)
        patient_list = models.Patient.objects.all()
        appointment_list = models.Appointment.objects.all().filter(doctor_id=doctor.id)
        return render(request, 'hms_app/index.html', {'is_patient':is_patient, 'is_doctor':is_doctor, 'appointment_list': appointment_list, 'doctor_status': doctor_status, 'patient_list': patient_list})
    else:
        return render(request, 'hms_app/index.html', {'is_patient':is_patient, 'is_doctor':is_doctor})

@login_required
def departments(request):
    department_list = models.Department.objects.all()
    doctor_list = models.Doctor.objects.all().filter(status=True)
    return render(request, 'hms_app/list_of_departments.html', {'department_list':department_list, 'doctor_list': doctor_list})

@login_required
def doctors(request):
    doctor_list = models.Doctor.objects.all()
    department_list = models.Department.objects.all()
    return render(request, 'hms_app/list_of_doctors.html', {'doctor_list':doctor_list, 'department_list':department_list})

@login_required
def patients(request):
    patient_list = models.Patient.objects.all()
    return render(request, 'hms_app/list_of_patients.html', {'patient_list':patient_list,})

@login_required
def appointments(request):
    appointment_list = models.Appointment.objects.all()
    patient_list = models.Patient.objects.all()
    doctor_list = models.Doctor.objects.all()
    department_list = models.Department.objects.all()
    return render(request, 'hms_app/list_of_appointments.html', {'appointment_list':appointment_list, 'patient_list':patient_list, 'doctor_list':doctor_list, 'department_list':department_list})

@login_required
def edit_doctor(request, doctor_id):
    edited = False
    doctor = models.Doctor.objects.get(id=doctor_id)
    doctor_form = forms.AdminEditDoctorForm(instance=doctor)
    if request.method=='POST':
        doctor_form = forms.AdminEditDoctorForm(instance=doctor, data=request.POST)
        if doctor_form.is_valid():
            doctor = doctor_form.save(commit=False)
            department = models.Department.objects.get(id=request.POST.get('department_id'))
            doctor.department_id = department.id
            doctor = doctor.save()
            edited = True
        else:
            print(doctor_form.errors)
    else:
        doctor_form = forms.AdminEditDoctorForm(instance=doctor)
    return render(request, 'hms_app/edit_doctor.html', {'doctor_form':doctor_form, 'doctor':doctor, 'edited':edited})

@login_required
def edit_department(request, department_id):
    edited = False
    department = models.Department.objects.get(id=department_id)
    department_form = forms.EditDepartmentForm(instance=department)
    if request.method=='POST':
        department_form = forms.EditDepartmentForm(instance=department, data=request.POST)
        if department_form.is_valid():
            department = department_form.save(commit=False)
            try:
                doctor = models.Doctor.objects.get(user_id=request.POST.get('doctor_id'))
                if doctor is None:
                    department.doctor_id = None
                else:
                    department.doctor_id = doctor.id
            except:
                pass
            department = department.save()
            edited = True
        else:
            print(department_form.errors)
    else:
        department_form = forms.EditDepartmentForm(instance=department)
    return render(request, 'hms_app/edit_department.html', {'department_form':department_form, 'department':department, 'edited':edited})

@login_required
def add_department(request):
    added = False
    dept_form = forms.DepartmentForm()
    if request.method == 'POST':
        dept_form = forms.DepartmentForm(request.POST)
        if dept_form.is_valid():
            department = dept_form.save()
            try:
                doctor = models.Doctor.objects.get(user_id=request.POST.get('doctor_id'))
                department.doctor_id = doctor.id
                department.save()
            except:
                department.save()
            added = True
        else:
            print(dept_form.errors)
    else:
        dept_form = forms.DepartmentForm()
    return render(request, 'hms_app/add_department.html', {'dept_form':dept_form, 'added':added})

@login_required
def logout(request):
    global is_patient 
    global is_doctor
    is_patient = False
    is_doctor = False
    django_logout(request)
    return HttpResponseRedirect(reverse('index'))

def admin_sign_up(request):
    signed_up = False
    user_form = forms.AdminUserForm()
    if request.method == 'POST':
        user_form = forms.AdminUserForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            signed_up = True
        else:
            print(user_form.errors)
    else:
        user_form = forms.AdminUserForm()
    return render(request, 'hms_app/admin_sign_up.html', {'user_form':user_form, 'signed_up':signed_up})

def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_superuser:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse('Your account is not active.')
        else:
            print("Someone tried to login and failed.")
            print("Username: {} and Password: {}".format(username, password))
            return HttpResponse("Invalid login details. Please try again.")
    else:
        return render(request, 'hms_app/admin_login.html', {})

def doctor_apply(request):
    applied = False
    user_form = forms.DoctorUserForm()
    doctor_form = forms.DoctorForm()
    if request.method=='POST':
        user_form = forms.DoctorUserForm(request.POST)
        doctor_form = forms.DoctorForm(request.POST, request.FILES)
        if user_form.is_valid and doctor_form.is_valid:
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            doctor = doctor_form.save(commit=False)
            department = models.Department.objects.get(id=request.POST.get('department_id'))
            doctor.department_id = department.id
            doctor.user = user
            doctor = doctor.save()
            applied = True
        else:
            print(user_form.errors, doctor_form.errors)
    else:
        user_form = forms.DoctorUserForm()
        doctor_form = forms.DoctorForm()
    return render(request, 'hms_app/doctor_application.html', {'user_form':user_form, 'doctor_form':doctor_form, 'applied':applied})

def patient_register(request):
    registered = False
    user_form = forms.PatientUserForm()
    patient_form = forms.PatientForm()
    if request.method=='POST':
        user_form = forms.PatientUserForm(request.POST)
        patient_form = forms.PatientForm(request.POST, request.FILES)
        if user_form.is_valid and patient_form.is_valid:
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            patient = patient_form.save(commit=False)
            patient.user = user 
            patient = patient.save()
            registered = True
        else:
            print(user_form.errors, patient_form.errors)
    else:
        user_form = forms.PatientUserForm()
        patient_form = forms.PatientForm()
    return render(request, 'hms_app/patient_registration.html', {'user_form':user_form, 'patient_form':patient_form, 'registered':registered})

def patient_login(request):
    global is_patient
    if request.method == 'POST':
        patient_username = request.POST.get('patient_username')
        patient_password = request.POST.get('patient_password')
        patient = authenticate(username=patient_username, password=patient_password)
        if patient:
            if patient.is_active:
                is_patient = True
                login(request, patient)
                return HttpResponseRedirect(reverse('index'), {'is_patient': is_patient,})
            else:
                return HttpResponse('Your account is not active.')
        else:
            print("Someone tried to login and failed.")
            print("Patient Username: {} and Patient Password: {}".format(patient_username, patient_password))
            return HttpResponse("Invalid login details. Please try again.")
    else:
        return render(request, 'hms_app/patient_login.html', {})

def doctor_login(request):
    global is_patient
    global is_doctor
    global doctor_status
    if request.method == 'POST':
        doctor_username = request.POST.get('doctor_username')
        doctor_password = request.POST.get('doctor_password')
        doctor = authenticate(username=doctor_username, password=doctor_password)
        if doctor:
            if doctor.is_active:
                is_doctor = True
                login(request, doctor)
                doc_status = models.Doctor.objects.get(user_id=request.user.id)
                doctor_status = doc_status.status
                return HttpResponseRedirect(reverse('index'), {'is_doctor': is_doctor, 'doctor_status': doctor_status})
            else:
                return HttpResponse('Your account is not active.')
        else:
            print("Someone tried to login and failed.")
            print("Doctor Username: {} and Doctor Password: {}".format(doctor_username, doctor_password))
            return HttpResponse("Invalid login details. Please try again.")
    else:
        return render(request, 'hms_app/doctor_login.html', {})

@login_required
def make_appointment(request):
    global is_patient
    appointed = False
    if is_patient:
        appointment_form = forms.PatientAppointmentForm()
        if request.method == 'POST':
            appointment_form = forms.PatientAppointmentForm(request.POST)
            if appointment_form.is_valid:
                appointment = appointment_form.save()
                doctor = models.Doctor.objects.get(user_id=request.POST.get('doctor_id'))
                appointment.doctor_id = doctor.id
                appointment.doctor_email = doctor.user.email
                patient = models.Patient.objects.get(user_id=request.user.id)
                appointment.patient_id = patient.id
                appointment.patient_email = patient.user.email
                appointment.save()
                appointed = True
            else:
                print(appointment_form.errors)
        else:
            appointment_form = forms.PatientAppointmentForm()
        return render(request, 'hms_app/patient_appointment.html', {'appointment_form': appointment_form, 'appointed': appointed, 'is_patient':is_patient})
    else:
        return HttpResponse("You are required to login.")

@login_required
def patient_edit_profile(request, user_id):
    global is_patient
    edited = False
    user = models.User.objects.get(id=user_id)
    patient = models.Patient.objects.get(user_id=user.id)
    user_form = forms.EditPatientUserForm(instance=user)
    patient_form = forms.EditPatientForm(instance=patient)
    if request.method=='POST':
        user_form = forms.EditPatientUserForm(instance=user, data=request.POST)
        patient_form = forms.EditPatientForm(instance=patient, data=request.POST)
        if user_form.is_valid() and patient_form.is_valid():
            user = user_form.save()
            user.save()
            patient = patient_form.save(commit=False)
            patient.user = user 
            try:
                patient.profile_pic = request.FILES['profile_pic']
            except:
                pass
            patient = patient.save()
            edited = True
        else:
            print(user_form.errors, patient_form.errors,)
    else:
        user_form = forms.EditPatientUserForm(instance=user)
        patient_form = forms.EditPatientForm(instance=patient)
    context = {'user_form':user_form, 'patient_form':patient_form, 'patient':patient, 'user':user, 'edited':edited, 'is_patient': is_patient}
    return render(request, 'hms_app/patient_edit_profile.html', context)

@login_required
def doctor_edit_profile(request, user_id):
    global is_doctor
    global doctor_status
    edited = False
    user = models.User.objects.get(id=user_id)
    doctor = models.Doctor.objects.get(user_id=user.id)
    user_form = forms.EditDoctorUserForm(instance=user)
    doctor_form = forms.EditDoctorForm(instance=doctor)
    if request.method == 'POST':
        user_form = forms.EditDoctorUserForm(instance=user, data=request.POST)
        doctor_form = forms.EditDoctorForm(instance=doctor, data=request.POST)
        if user_form.is_valid() and doctor_form.is_valid():
            user = user_form.save()
            user.save()
            doctor = doctor_form.save(commit=False)
            doctor.user = user
            department = models.Department.objects.get(id=request.POST.get('department_id'))
            doctor.department_id = department.id
            try:
                doctor.profile_pic = request.FILES['profile_pic']
            except:
                pass
            doctor = doctor.save()
            edited = True
        else:
            print(user_form.errors, doctor_form.errors,)
    else:
        user_form = forms.EditDoctorUserForm(instance=user)
        doctor_form = forms.EditDoctorForm(instance=doctor)
    context = {'user_form':user_form, 'doctor_form':doctor_form, 'doctor':doctor, 'user':user, 'edited':edited, 'is_doctor': is_doctor, 'doctor_status':doctor_status}
    return render(request, 'hms_app/doctor_edit_profile.html', context)

@login_required
def patient_edit_appointment(request, appointment_id):
    global is_patient
    edited = False
    appointment = models.Appointment.objects.get(id=appointment_id)
    appointment_form = forms.PatientEditAppointmentForm(instance=appointment)
    if request.method == 'POST':
        appointment_form = forms.PatientEditAppointmentForm(instance=appointment, data=request.POST)
        if appointment_form.is_valid():
            appointment = appointment_form.save()
            doctor = models.Doctor.objects.get(user_id=request.POST.get('doctor_id'))
            appointment.doctor_id = doctor.id
            appointment.doctor_email = doctor.user.email
            patient = models.Patient.objects.get(user_id=request.user.id)
            appointment.patient_id = patient.id
            appointment.patient_email = patient.user.email
            appointment.save()
            edited = True
        else:
            print(appointment_form.errors,)
    else:
        appointment_form = forms.PatientEditAppointmentForm(instance=appointment)
    context = {'appointment_form':appointment_form, 'appointment':appointment, 'edited':edited, 'is_patient':is_patient}
    return render(request, 'hms_app/patient_edit_appointment.html', context)

@login_required
def delete_appointment(request, appointment_id):
    global is_patient
    deleted = False
    appointment = models.Appointment.objects.get(id=appointment_id)
    appointment.delete()
    deleted = True
    return render(request, 'hms_app/patient_edit_appointment.html', {'is_patient':is_patient, 'deleted':deleted})

@login_required
def delete_department(request, department_id):
    department = models.Department.objects.get(id=department_id)
    department.delete()
    deleted = True
    return render(request, 'hms_app/edit_department.html', {'deleted':deleted,})

@login_required
def remove_head(request, department_id):
     department = models.Department.objects.get(id=department_id)
     department.doctor_id = None
     department.save()
     removed = True
     return render(request, 'hms_app/edit_department.html', {'removed':removed,})

@login_required
def delete_patient(request, patient_id):
    patient = models.Patient.objects.get(id=patient_id)
    user = models.User.objects.get(id=patient.user_id)
    try:
        appointments = models.Appointment.objects.get(patient_id=patient_id)
        appointments.delete()
    except:
        pass
    patient.delete()
    user.delete()
    deleted = True
    return render(request, 'hms_app/list_of_patients.html', {'deleted':deleted,})

@login_required
def delete_doctor(request, doctor_id):
    doctor = models.Doctor.objects.get(id=doctor_id)
    user = models.User.objects.get(id=doctor.user_id)
    try:
        appointments = models.Appointment.objects.get(doctor_id=doctor.id)
        appointments.delete()
        appointments.save()
    except:
        pass
    try:
        departments = models.Department.objects.get(doctor_id=doctor.id)
        departments.doctor_id = None
        departments.save()
    except:
        pass
    doctor.delete()
    user.delete()
    deleted = True
    return render(request, 'hms_app/edit_doctor.html', {'deleted':deleted,})

@login_required
def doctor_edit_appointment(request, appointment_id):
    global is_doctor
    global doctor_status
    edited = False
    appointment = models.Appointment.objects.get(id=appointment_id)
    appointment_form = forms.DoctorEditAppointmentForm(instance=appointment)
    if request.method == 'POST':
        appointment_form = forms.DoctorEditAppointmentForm(instance=appointment, data=request.POST)
        if appointment_form.is_valid():
            appointment = appointment_form.save()
            appointment.save()
            edited = True
        else:
            print(appointment_form.errors,)
    else:
        appointment_form = forms.DoctorEditAppointmentForm(instance=appointment)
    context = {'appointment_form':appointment_form, 'appointment':appointment, 'edited':edited, 'is_doctor':is_doctor, 'doctor_status':doctor_status}
    return render(request, 'hms_app/doctor_edit_appointment.html', context)

@login_required
def view_doctor_profile(request, doctor_id):
    global is_patient
    doctor = models.Doctor.objects.get(id=doctor_id)
    department = models.Department.objects.get(id=doctor.department_id)
    return render(request, 'hms_app/view_doctor_profile.html', {'doctor':doctor, 'department':department, 'is_patient':is_patient})

@login_required
def view_patient_profile(request, patient_id):
    global is_doctor
    global doctor_status
    patient = models.Patient.objects.get(id=patient_id)
    return render(request, 'hms_app/view_patient_profile.html', {'patient':patient, 'is_doctor':is_doctor, 'doctor_status':doctor_status})

@login_required
def patient_profile(request): 
    global is_patient
    return render(request, 'hms_app/patient_profile.html', {'is_patient':is_patient})

@login_required
def doctor_profile(request):
    global is_doctor
    global doctor_status
    department_list = models.Department.objects.all()
    return render(request, 'hms_app/doctor_profile.html', {'is_doctor':is_doctor, 'doctor_status':doctor_status, 'department_list':department_list})