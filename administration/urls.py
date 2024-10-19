from django.urls import path

from . import views


urlpatterns = [
    path("dashboard/", views.AdminDashboard.as_view(), name="admin_dashboard"),
    path("list/groups/", views.GroupListView.as_view(), name="group_list"),
    path("add/groups/", views.GroupCreateView.as_view(), name="group_add"),
    path("update/groups/<int:pk>/", views.GroupUpdateView.as_view(), name="group_update"),
    path("delete/groups/<int:pk>/", views.GroupDeleteView.as_view(), name="group_delete"),
    path("groups/permissions/<int:group_id>/", views.group_permissions, name="group_permissions"),
]
