from django.shortcuts import render, redirect
from . serializers import PatientSerializer, DoctorSerializer, UserSerializer
from . models import Patient, Doctor, Prescriptions
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, mixins
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from rest_framework.renderers import TemplateHTMLRenderer
from django.shortcuts import get_object_or_404
from . forms import PatientSignupForm, DoctorSignupForm, PrescriptionForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.db.models import Q
from django.http import HttpResponse
from django.views.generic import View
from .process import html_to_pdf 
from django.template.loader import render_to_string
from django.core.paginator import Paginator
from django.contrib import messages
# Create your views here.

def home(request):
    patient = Patient.objects.all()
    doctor = Doctor.objects.all()
    context = {"patient": patient, "doctor": doctor}
    return render(request, "home.html", context)

def patient_register(request):
    form = PatientSignupForm()
    if request.method=='POST':
        form = PatientSignupForm(request.POST)
        if form.is_valid():
            obj=form.save()
            login(request, obj, backend='django.contrib.auth.backends.ModelBackend')
            return redirect("patient-add")
    context = {"form": form}
    return render(request, "patient_register.html", context)

def doctor_register(request):
    form = DoctorSignupForm()
    if request.method=='POST':
        form = DoctorSignupForm(request.POST)
        if form.is_valid():
            obj=form.save()
            login(request, obj, backend='django.contrib.auth.backends.ModelBackend')
            return redirect("doctor-add")
    context = {"form": form}
    return render(request, "doctor_register.html", context)

@login_required(login_url='login')
def patient_profile(request, username):
    patient = Patient.objects.get(user=request.user)
    prescriptions = Prescriptions.objects.filter(prescribe_for=patient)
    context = {"patient": patient, "prescriptions": prescriptions}
    return render(request, "patient_profile.html", context)
    

class Profile(View):
    def get(self, request, *args, **kwargs):
        user = User.objects.get(username=self.request.user)
        patient = Patient.objects.filter(user=self.request.user)
        doctor = Doctor.objects.filter(user=self.request.user)
        if patient:
            return redirect("patient-profile", user)
        elif doctor:
            return redirect("doctor-profile", user)
        

@login_required(login_url='login')
def doctor_profile(request, username):
    doctor = Doctor.objects.get(user=request.user)
    context = {"doctor": doctor}
    return render(request, "doctor_profile.html", context)


def create_prescription(request, slug):
    form = PrescriptionForm()
    user = Doctor.objects.get(slug=slug)
    if request.method == 'POST':
        form = PrescriptionForm(request.POST)
        searched = request.POST.get("q")
        if form.is_valid:
            obj = form.save(commit=False)
            obj.prescribed_by = user
            userr = searched
            obj.save()
            print(userr)
        return redirect('home')
    context = {'form': form}
    return render(request, "create_prescrptions.html", context)



class PatientList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'patient_list.html'

    def get(self, request):
        p = Paginator(Patient.objects.all().order_by("-id"), 2)
        page = request.GET.get('page')
        queryset = p.get_page(page)
        return Response({'patients': queryset})

class DoctorList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'doctor_list.html'

    def get(self, request):
        p = Paginator(Doctor.objects.all().order_by("-id"), 2)
        page = request.GET.get('page')
        queryset = p.get_page(page)
        return Response({'doctors': queryset})



class CreatePatient(mixins.CreateModelMixin,generics.GenericAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            serializer = PatientSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors)
        serializer.save(user=request.user)

        return redirect('home')

class CreateDoctor(mixins.CreateModelMixin,generics.GenericAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            serializer = DoctorSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors)
        serializer.save(user=request.user)
        
        return redirect('home')


class PatientRetrieve(LoginRequiredMixin,generics.RetrieveAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    lookup_fields = 'slug'
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'patient_detail.html'
    login_url = '/login/'


    def get(self, request, slug):
        queryset = Patient.objects.get(slug=slug)
        prescriptions = Prescriptions.objects.filter(prescribe_for=queryset)
        return Response({'patient': queryset, 'prescriptions': prescriptions})

class DoctorRetrieve(generics.RetrieveAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    lookup_fields = 'slug'
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'Doctor_detail.html'

    def get(self, request, slug):
        queryset = Doctor.objects.get(slug=slug)
        return Response({'doctor': queryset})

class PatientUpdate(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'patient_update.html'

    def get(self, request, slug):
        patient = get_object_or_404(Patient, slug=slug, user=request.user)
        serializer = PatientSerializer(patient)
        return Response({'serializer': serializer, 'patient': patient})

    def post(self, request, slug):
        patient = get_object_or_404(Patient, slug=slug)
        serializer = PatientSerializer(patient, data=request.data)
        if not serializer.is_valid():
            return Response({'serializer': serializer, 'patient': patient})
        serializer.save()
        messages.success(request, 'Your profile was updated')
        return redirect('patient-profile', 'username')

class DoctorUpdate(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'doctor_update.html'
    

    def get(self, request, slug):
        doctor = get_object_or_404(Doctor, slug=slug, user=request.user)
        serializer = DoctorSerializer(doctor)
        return Response({'serializer': serializer, 'doctor': doctor})

    def post(self, request, slug):
        doctor = get_object_or_404(Doctor, slug=slug)
        serializer = DoctorSerializer(doctor, data=request.data)
        if not serializer.is_valid():
            return Response({'serializer': serializer, 'doctor': doctor})
        serializer.save()
        messages.success(request, 'Your profile was updated')
        return redirect('doctor-profile', 'username')
    
        

class PatientDelete(generics.RetrieveDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'

class DoctorDelete(generics.RetrieveDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    
    
def search(request):
    if request.method == 'POST':
        searched = request.POST['q']
        patients = Patient.objects.filter(
            Q(first_name__icontains=searched)|
            Q(last_name__icontains= searched)
        )

    return render(request, "search.html", {"searched": searched, "patients": patients })

class GeneratePdf(View):
     def get(self, request, slug, *args, **kwargs):
        patient = Patient.objects.get(slug=slug)
        prescriptions = Prescriptions.objects.filter(prescribe_for=patient)
        open('templates/temp.html', "w").write(render_to_string('patient_profile.html', {'patient': patient, 'prescriptions': prescriptions}))

        # Converting the HTML template into a PDF file
        pdf = html_to_pdf('temp.html')
         
         # rendering the template
        return HttpResponse(pdf, content_type='application/pdf')