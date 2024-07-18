from django.contrib import admin
from . models import Patient, Prescriptions, Doctor, Document, CompressedDICOMFile
# Register your models here.

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display=['first_name', 'last_name', 'email', 'phone_number', 'medical_conditions','current_medications']
    search_fields=['first_name', 'last_name', 'email', 'phone_number', 'prescriptions__name']

@admin.register(Prescriptions)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ['medication', 'prescribed_by', 'prescribed_on']
    list_filter = ['prescribed_on']
    search_fields = ['name', 'prescribed_by']

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'specialization', 'language', 'email']
    search_fields = ['first_name', 'last_name', 'specialization']

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    search_fields = ['user__username']

@admin.register(CompressedDICOMFile)
class CompressedDICOMFileAdmin(admin.ModelAdmin):
    list_display = ['original_file', 'compressed_file']
    
