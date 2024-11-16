from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.timezone import localdate
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


class SupplierListView(ListView):
    paginate_by = 10
    ordering = ["id"]
    model = Supplier
    template_name = "inventory/list_supplier.html"
    context_object_name = "suppliers"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Supplier List"
        return context


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


class SupplierDeleteView(DeleteView):
    model = Supplier
    success_url = reverse_lazy("list_supplier")

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Supplier deleted successfully.")
        return super().delete(request, *args, **kwargs)


class RouteOfAdministrationListView(ListView):
    paginate_by = 10
    ordering = ["id"]
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


class RouteOfAdministrationDeleteView(DeleteView):
    model = RouteOfAdministration
    success_url = reverse_lazy("list_route_of_administration")

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Route of administration deleted successfully.")
        return super().delete(request, *args, **kwargs)


class MedicineListView(ListView):
    paginate_by = 10
    ordering = ["id"]
    model = Medicine
    template_name = "inventory/medicine_list.html"
    context_object_name = "medicines"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Medicine List"
        context["routes"] = RouteOfAdministration.objects.all()
        context["storage_locations"] = Medicine.objects.values_list(
            "storage_location", flat=True
        ).distinct()
        return context

    def get_queryset(self):
        query = self.request.GET.get("search", "")
        route = self.request.GET.get("route", "")
        location = self.request.GET.get("location", "")
        expiration = self.request.GET.get("expiration", "")

        queryset = Medicine.objects.all()

        # Search filter
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query)
                | Q(generic_name__icontains=query)
                | Q(brand_name__icontains=query)
            )

        if route:
            queryset = queryset.filter(route_of_administration__id=route)

        if location:
            queryset = queryset.filter(storage_location__icontains=location)

        if expiration == "expiring_today":
            today = localdate()  # Use current local date
            queryset = queryset.filter(expiration_date=today)
        elif expiration == "expiring_this_month":
            today = localdate()
            queryset = queryset.filter(
                expiration_date__month=today.month, expiration_date__year=today.year
            )

        return queryset

    def get(self, request, *args, **kwargs):
        # Check if the request is an AJAX request
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            medicines = self.get_queryset()
            return JsonResponse({"medicines": list(medicines.values())})

        return super().get(request, *args, **kwargs)


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
    paginate_by = 10
    ordering = ["id"]
    model = MedicineSupplier
    template_name = "inventory/medicine_supplier_list.html"
    context_object_name = "medicine_suppliers"

    def get_queryset(self):
        queryset = super().get_queryset()
        medicine = self.request.GET.get("medicine")
        supplier = self.request.GET.get("supplier")
        supply_date = self.request.GET.get("supply_date")

        if medicine:
            queryset = queryset.filter(medicine_id=medicine)
        if supplier:
            queryset = queryset.filter(supplier_id=supplier)
        if supply_date:
            queryset = queryset.filter(supply_date=supply_date)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Medicine supplier list"
        context["medicines"] = Medicine.objects.all()
        context["suppliers"] = Supplier.objects.all()
        return context

    def get(self, request, *args, **kwargs):
        try:
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                queryset = self.get_queryset()
                data = {
                    "medicine_suppliers": list(
                        queryset.values(
                            "id",
                            "supplier__name",
                            "medicine__name",
                            "price",
                            "supply_date",
                        )
                    )
                }
                return JsonResponse(data)
        except Exception as e:
            print(f"Error in AJAX view: {e}")
            return JsonResponse({"error": str(e)}, status=500)

        return super().get(request, *args, **kwargs)


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
