from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from .models import PatientDetails
from accounts.froms import CustomUserCreationForm, PatientForm
from django.contrib import messages
from django.http import JsonResponse

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

# Create a patient (CreateView)
class PatientCreateView(CreateView):
    model = PatientDetails
    form_class = PatientForm
    template_name = 'patient_list.html'
    success_url = reverse_lazy('patient_list')

    def form_valid(self, form):
        messages.success(self.request, "Patient created successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "There was an error creating the patient. Please check the form for errors.")
        patients = PatientDetails.objects.all()  # Assuming you want to show all patients
        context = self.get_context_data(form=form)
        context['patients'] = patients  # Include patients in context to render the list

        return self.render_to_response(context) 
    
# List all patients (ListView)
class PatientListView(ListView):
    model = PatientDetails
    template_name = 'patient_list.html'
    context_object_name = 'patients'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PatientForm()  # Pass the form instance here
        return context

# View a single patient's details (DetailView)
class PatientDetailView(DetailView):
    model = PatientDetails
    template_name = 'patient_detail.html'
    context_object_name = 'patient'

# Update a patient's details (UpdateView)
class PatientUpdateView(UpdateView):
    model = PatientDetails
    form_class = PatientForm
    template_name = 'patient_list.html'
    success_url = reverse_lazy('patient_list')

    def form_valid(self, form):
        patient = form.save()  # Save the patient details
        return JsonResponse({
            'status': 'success',
            'username': patient.username,
            'address': patient.address,
            'phone_number': patient.phone_number,
            'condition': patient.condition,
        })

    def form_invalid(self, form):
        return JsonResponse({'status': 'error', 'errors': form.errors})


# Delete a patient (DeleteView)
class PatientDeleteView(DeleteView):
    model = PatientDetails
    template_name = 'patient_confirm_delete.html'
    success_url = reverse_lazy('patient_list')