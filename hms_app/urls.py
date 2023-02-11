from .views import PasswordsChangeView
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

app_name = 'hms_app'

urlpatterns = [
    path('list_of_appointments/', views.appointments, name='appointments'),
    path('list_of_departments/', views.departments, name='departments'),
    path('add_department/', views.add_department, name='add_department'),
    path('edit_department/<int:department_id>', views.edit_department, name='edit_department'),
    path('list_of_doctors/', views.doctors, name='doctors'),
    path('edit_doctor/<int:doctor_id>', views.edit_doctor, name="edit_doctor"),
    path('list_of_patients/', views.patients, name='patients'),
    path('patient_register/', views.patient_register, name='patient_register'),
    path('doctor_apply/', views.doctor_apply, name='doctor_apply'),
    path('patient_login/', views.patient_login, name='patient_login'),
    path('doctor_login/', views.doctor_login, name='doctor_login'),
    path('patient_appointment/', views.make_appointment, name='patient_appointment'),
    path('patient_profile/', views.patient_profile, name='patient_profile'),
    path('doctor_profile/', views.doctor_profile, name='doctor_profile'),
    path('patient_edit_profile/<int:user_id>', views.patient_edit_profile, name="patient_edit_profile"),
    path('doctor_edit_profile/<int:user_id>', views.doctor_edit_profile, name="doctor_edit_profile"),
    path('patient_edit_appointment/<int:appointment_id>', views.patient_edit_appointment, name='patient_edit_appointment'),
    path('doctor_edit_appointment/<int:appointment_id>', views.doctor_edit_appointment, name='doctor_edit_appointment'),
    path('view_doctor_profile/<int:doctor_id>', views.view_doctor_profile, name='view_doctor_profile'),
    path('view_patient_profile/<int:patient_id>', views.view_patient_profile, name='view_patient_profile'),
    path('password/', PasswordsChangeView.as_view(), name='change_password'),
    path('password_changed/', views.password_changed, name='password_changed'),
    path('appointment_deleted/<int:appointment_id>', views.delete_appointment, name='delete_appointment'),
    path('department_deleted/<int:department_id>', views.delete_department, name='delete_department'),
    path('patient_deleted/<int:patient_id>', views.delete_patient, name='delete_patient'),
    path('doctor_deleted/<int:doctor_id>', views.delete_doctor, name='delete_doctor'),
    path('head_removed/<int:department_id>', views.remove_head, name='remove_head'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)