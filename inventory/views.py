from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    ListView,
    TemplateView,
    UpdateView,
)

from .forms import (
    MedicineForm,
    MedicineSupplierForm,
    RouteOfAdministrationForm,
    SupplierForm,
)
from .models import Medicine, MedicineSupplier, RouteOfAdministration, Supplier


class InventoryDashboard(TemplateView):
    template_name = "inventory/inventory_dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Inventory Dashboard"
        context["total_medicines"] = Medicine.objects.all().count()
        context["total_suppliers"] = Supplier.objects.all().count()
        context["total_medicine_suppliers"] = MedicineSupplier.objects.all().count()
        return context


# List View for Suppliers
class SupplierListView(ListView):
    model = Supplier
    template_name = "inventory/list_supplier.html"
    context_object_name = "suppliers"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Supplier List"
        return context


# Create View for Suppliers
class SupplierCreateView(CreateView):
    model = Supplier
    form_class = SupplierForm
    template_name = "inventory/add_update_template.html"
    success_url = reverse_lazy("list_supplier")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Add Supplier"
        context["action"] = "Add "
        context["model"] = "Supplier "
        return context

    def form_valid(self, form):
        messages.success(self.request, "Supplier created successfully.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Failed to create supplier.")
        return super().form_invalid(form)


# Update View for Suppliers
class SupplierUpdateView(UpdateView):
    model = Supplier
    form_class = SupplierForm
    template_name = "inventory/add_update_template.html"
    success_url = reverse_lazy("list_supplier")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Update Supplier"
        context["action"] = "Update "
        context["model"] = "Supplier "
        return context

    def form_valid(self, form):
        messages.success(self.request, "Supplier updated successfully.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Failed to update supplier.")
        return super().form_invalid(form)


# Delete View for Suppliers
class SupplierDeleteView(DeleteView):
    model = Supplier
    success_url = reverse_lazy("list_supplier")

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Supplier deleted successfully.")
        return super().delete(request, *args, **kwargs)


class RouteOfAdministrationListView(ListView):
    model = RouteOfAdministration
    template_name = "inventory/routes_of_administration_list.html"
    context_object_name = "routes"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Route of administration list"
        return context


class RouteOfAdministrationCreateView(CreateView):
    model = RouteOfAdministration
    form_class = RouteOfAdministrationForm
    template_name = "inventory/add_update_template.html"
    success_url = reverse_lazy("list_route_of_administration")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Add Route Of Administration"
        context["action"] = "Add "
        context["model"] = "Route Of Administration "
        return context

    def form_valid(self, form):
        messages.success(self.request, "Route of administration created successfully.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Failed to create route of administration.")
        return super().form_invalid(form)


# Update View for RouteOfAdministration
class RouteOfAdministrationUpdateView(UpdateView):
    model = RouteOfAdministration
    form_class = RouteOfAdministrationForm
    template_name = "inventory/add_update_template.html"
    success_url = reverse_lazy("list_route_of_administration")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Update Route Of Administration"
        context["action"] = "Update "
        context["model"] = "Route Of Administration "
        return context

    def form_valid(self, form):
        messages.success(self.request, "Route of administration updated successfully.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Failed to update route of administration.")
        return super().form_invalid(form)


# Delete View for RouteOfAdministration
class RouteOfAdministrationDeleteView(DeleteView):
    model = RouteOfAdministration
    success_url = reverse_lazy("list_route_of_administration")

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Route of administration deleted successfully.")
        return super().delete(request, *args, **kwargs)


class MedicineListView(ListView):
    model = Medicine
    template_name = "inventory/medicine_list.html"
    context_object_name = "medicines"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Medicine list"
        return context


# Create View for Medicine
class MedicineCreateView(CreateView):
    model = Medicine
    form_class = MedicineForm
    template_name = "inventory/add_update_template.html"
    success_url = reverse_lazy("list_medicine")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Add Medicine"
        context["action"] = "Add "
        context["model"] = "Medicine"
        return context

    def form_valid(self, form):
        messages.success(self.request, "Medicine created successfully.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Failed to create medicine.")
        return super().form_invalid(form)


# Update View for Medicine
class MedicineUpdateView(UpdateView):
    model = Medicine
    form_class = MedicineForm
    template_name = "inventory/add_update_template.html"
    success_url = reverse_lazy("list_medicine")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Update Medicine"
        context["action"] = "Update "
        context["model"] = "Medicine"
        return context

    def form_valid(self, form):
        messages.success(self.request, "Medicine updated successfully.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Failed to update Medicine.")
        return super().form_invalid(form)


# Delete View for Medicine
class MedicineDeleteView(DeleteView):
    model = Medicine
    success_url = reverse_lazy("list_medicine")

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Medicine deleted successfully.")
        return super().delete(request, *args, **kwargs)


class MedicineSupplierListView(ListView):
    model = MedicineSupplier
    template_name = "inventory/medicine_supplier_list.html"
    context_object_name = "medicine_suppliers"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Medicine supplier list"
        return context


# Create View for Medicine Supplier
class MedicineSupplierCreateView(CreateView):
    model = MedicineSupplier
    form_class = MedicineSupplierForm
    template_name = "inventory/add_update_template.html"
    success_url = reverse_lazy("list_medicine_supplier")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Add Medicine Supplier"
        context["action"] = "Add "
        context["model"] = "Medicine Supplier"
        return context

    def form_valid(self, form):
        messages.success(self.request, "Medicine Supplier created successfully.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Failed to create medicine supplier.")
        return super().form_invalid(form)


# Update View for Medicine Supplier
class MedicineSupplierUpdateView(UpdateView):
    model = MedicineSupplier
    form_class = MedicineSupplierForm
    template_name = "inventory/add_update_template.html"
    success_url = reverse_lazy("list_medicine_supplier")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Update Medicine Supplier"
        context["action"] = "Update"
        context["model"] = "Medicine Supplier"
        return context

    def form_valid(self, form):
        messages.success(self.request, "Medicine supplier updated successfully.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Failed to update medicine supplier.")
        return super().form_invalid(form)


# Delete View for Medicine Supplier
class MedicineSupplierDeleteView(DeleteView):
    model = Medicine
    success_url = reverse_lazy("list_medicine_supplier")

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Medicine supplier deleted successfully.")
        return super().delete(request, *args, **kwargs)
