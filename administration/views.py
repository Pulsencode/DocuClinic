from django.contrib.auth.models import Group, Permission
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView
)
from django.urls import reverse_lazy
from django.contrib import messages


class AdminDashboard(TemplateView):
    template_name = "administration/admin_dashboard.html"


class GroupListView(ListView):
    model = Group
    template_name = "administration/group_list.html"
    context_object_name = "groups"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Group List"
        return context


class GroupCreateView(CreateView):
    model = Group
    template_name = "administration/group_list.html"
    fields = ["name"]
    success_url = reverse_lazy("group_list")

    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except Exception as e:
            print(str(e))
            messages.error(
                self.request,
                "This group name already exists. Please choose a different name.",
            )
            return self.form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.errors, "Please correct the errors below.")
        return super().form_invalid(form)


class GroupUpdateView(UpdateView):
    model = Group
    fields = ["name"]
    template_name = "administration/group_list.html"
    success_url = reverse_lazy("group_list")

    def form_valid(self, form):
        try:
            messages.success(self.request, "Group updated successfully.")
            return super().form_valid(form)
        except Exception as e:
            form.add_error((e), "A group with this name already exists.")
            return self.form_invalid(form)

    def form_invalid(self, form):
        messages.error(
            self.request, form.errors, "There was an error updating the group."
        )
        return super().form_invalid(form)


class GroupDeleteView(DeleteView):
    model = Group
    template_name = "administration/group_list.html"
    success_url = reverse_lazy("group_list")

    def delete(self, request, *args, **kwargs):
        messages.success(request, "The group was successfully deleted.")
        return super().delete(request, *args, **kwargs)


def group_permissions(request, group_id):
    group = get_object_or_404(Group, id=group_id)

    excluded_apps = ["admin", "auth", "contenttypes", "sessions", "log"]
    excluded_models = [
        "permission",
        "group",
        "user",
        "contenttype",
        "session",
        "logentry",
    ]

    permissions = (
        Permission.objects.exclude(content_type__app_label__in=excluded_apps)
        .exclude(content_type__model__in=excluded_models)
        .select_related("content_type")
    )

    if request.method == "POST":
        selected_permissions = request.POST.getlist("permissions")
        group.permissions.set(selected_permissions)
        messages.success(request, f"Permissions updated for group '{group.name}'.")
        return redirect("group_list")

    context = {
        "page_title": "Group Permission",
        "group": group,
        "permissions": permissions,
        "assigned_permissions": group.permissions.values_list("id", flat=True),
    }

    return render(request, "administration/group_permission.html", context)
