from django.urls import path
from .views import InventoryDashboard

urlpatterns = [
    path("dashboard/", InventoryDashboard.as_view(), name="inventory_dashboard"),
]
