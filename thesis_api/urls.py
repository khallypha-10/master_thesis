from django.urls import path
from . import views
from django.conf import settings
from django.contrib.staticfiles.urls import static

urlpatterns = [
    path('home', views.home, name="home"),
    path('patients', views.PatientList.as_view(), name="patients"),
    path('doctors', views.DoctorList.as_view(), name="doctors"),
    path('patient-details/<slug>', views.PatientRetrieve.as_view(), name="patient-details"),
    path('patient-update/<slug>', views.PatientUpdate.as_view(), name="patient"),
    path('patient-delete/<username>', views.PatientDelete.as_view(), name="patient-delete"),
    path('patient-add', views.CreatePatient.as_view(), name="patient-add"),
    path('doctor-add', views.CreateDoctor.as_view(), name="doctor-add"),
    path('patient-profile/<str:username>/', views.patient_profile, name="patient-profile"),
    path('profile/<str:username>/', views.Profile.as_view(), name="profile"),
    path('doctor-profile/<str:username>/', views.doctor_profile, name="doctor-profile"),
    path('doctor-update/<slug>', views.DoctorUpdate.as_view(), name="doctor"),
    path('doctor-details/<slug>/', views.DoctorRetrieve.as_view(), name="doctor-details"),
    path('patient-register', views.patient_register, name="patient-register"),
    path('doctor-register', views.doctor_register, name="doctor-register"),
    path('doctor-delete/<username>', views.DoctorDelete.as_view(), name="doctor-delete"),
    path('prescribe/<slug>', views.create_prescription, name="prescribe"),
    path('search', views.search, name="search"),
    path('pdf/<slug>', views.GeneratePdf.as_view(), name="generate-pdf"),     
    path('document-upload', views.list, name="document-upload"),     
]

urlpatterns +=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_URL)