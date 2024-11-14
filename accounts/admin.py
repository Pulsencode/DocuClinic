from django.contrib import admin

from .models import Accountant, Administrator, Nurse, Patient, Physician, Receptionist, PatientDetail, Weekday, PhysicianAvailability

# admin.site.register(User) # Do not create users with this model
admin.site.register(Administrator)
admin.site.register(Physician)
admin.site.register(Accountant)
admin.site.register(Patient)
admin.site.register(Nurse)
admin.site.register(Receptionist)
admin.site.register(PatientDetail)
admin.site.register(Weekday)


@admin.register(PhysicianAvailability)
class PhysicianAvailabilityAdmin(admin.ModelAdmin):
    list_display = ('physician', 'display_work_days', 'work_time_start', 'work_time_end', 'lunch_start', 'lunch_end')

    def display_work_days(self, obj):
        return ", ".join([day.name for day in obj.work_days.all()])
    display_work_days.short_description = 'Work Days' 