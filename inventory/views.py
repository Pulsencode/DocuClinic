from django.shortcuts import render
from django.views import View


class InventoryDashboard(View):
    template_name = "inventory/inventory_dashboard.html"

    def get(self, request):
        return render(request, self.template_name)
