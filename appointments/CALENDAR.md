# Appointment calendar

The appointment admin list at `/management/appointments/appointment/` now opens a Sunday–Saturday weekly calendar. A mini month calendar, Today, Previous/Next, and the Week/Month/Day selector change the visible dates. Patient search, physician and status filters apply to the displayed period. All times are in the clinic timezone, regardless of the browser's timezone.

Week and Day views position events by their saved local date and time on a 24-hour axis. Overlapping appointments use separate lanes; short events have a minimum readable height. Month view shows events inside each date. On narrow screens, the filters can be expanded and the week grid scrolls horizontally, retaining all seven days; Day view provides a compact alternative.

Click or keyboard-activate an event for its details dialog. Escape or Close dismisses it and returns focus to the event. **View/Edit Details** opens the existing appointment admin form, with its normal permissions. Appointment type/reason is displayed as **Not recorded** because the model does not store it. No schema or appointment data changes are made by this feature.

The event display uses the stored duration. Legacy appointments without a duration use the current clinic duration, or a 30-minute display fallback if that is not configured; the dialog labels this estimate. Legacy events spanning midnight continue into the following day. Appointments without a date/time are flagged and remain accessible through **List tools & bulk actions**, which also retains Django's search, filters, pagination and existing actions. Existing bookmarked admin filter/search URLs still work. Cancelled appointments remain visible and are distinguished by status.

Calendar pages and feeds require appointment view/change permission. Patient and physician names, filters, and searches require their own related model view/change permissions, including group permissions. Denied related tables are not joined by the event feed. Creation requires the existing appointment-add rules. The existing table and edit screens retain their own admin behavior.

The removed custom booking-form template is not restored: the appointment admin falls back to the standard Unfold/Django form. No new library, external calendar integration or migration is required for this list UI.

Checks: `venv/Scripts/python.exe manage.py test appointments`, `manage.py check`, configured pre-commit hooks, and browser review with synthetic data in an isolated database. Never migrate or seed the clinic database merely to preview the calendar.
