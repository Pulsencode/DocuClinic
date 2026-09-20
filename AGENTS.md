# DocuClinic AI rule book

Keep changes small, understandable, and safe for existing clinic records. These rules apply throughout this repository. Read `PROJECT_FINDINGS.md` for known issues; check current code before assuming an issue still exists.

## Know the current design

- This is a Django project using django-unfold for the staff admin at `/management/`.
- `accounts.User` is for staff login. `accounts.Patient` is a separate patient record.
- Current staff roles are administrator, physician, nurse, and receptionist.
- Prescriptions already link to patients and physicians.
- `/` is the public landing page. Older custom staff views/forms are mostly inactive.
- Accounting is not an active app. Keep new work within the requested scope.

## Do

1. **Read before editing.** Check the affected model, admin, settings, templates, migrations, and tests. Check `git status` and preserve other people's work.
2. **Follow the existing Django structure.** Put data in models, admin presentation in `admin.py`, page markup in templates, and shared admin settings in `core/settings/unfold.py`.
3. **Keep business rules reusable.** Put field rules in model validation and multi-step operations in a small shared function when needed. Enforce rules on the server, including writes from commands.
4. **Use the actual models.** Patients have names and registration IDs, not usernames or login methods. Use `settings.AUTH_USER_MODEL` for new staff relations and `get_user_model()` when resolving the staff model at runtime.
5. **Update connected code together.** A field change may affect searches, autocomplete, display methods, dashboard queries, templates, seed commands, migrations, and documentation.
6. **Protect access to records.** Use Django permissions and the agreed record-access rules for pages, queries, dashboards, actions, and autocomplete. Test ordinary staff as well as superusers.
7. **Protect data during schema changes.** Create migrations, explain how existing records are mapped, and check upgrades with representative test data. An empty database is not enough for a relationship change.
8. **Use predictable data types.** Use decimal values for fractional money, timezone-aware dates, clear units, and appropriate validators. Confirm clinical and billing rules before implementing them.
9. **Keep database work efficient.** Use `select_related()` for displayed foreign keys, `prefetch_related()` for collections, and database counts/aggregates. Use transactions for changes that must succeed together.
10. **Explain the result plainly.** Report what changed, why, what was checked, and any remaining failures. Update documentation when behavior changes.

## Admin panel rules

- Use Unfold `ModelAdmin` and Unfold inline classes for new admin screens. Keep Django's `UserAdmin` behavior for staff accounts and password handling.
- Add useful list columns, search, and filters. Use readable field groups; use tabs when a form is long.
- Keep generated IDs, calculated values, and system timestamps read-only.
- Use autocomplete for large related lists, and ensure the related admin has valid search fields. Confirm selectable records meet the intended role and active-state rules.
- Use named URLs with `reverse()`, `reverse_lazy()`, or the template `url` tag. Keep sidebar labels accurate.
- Give every model link in `core/settings/unfold.py` an Unfold permission callback for the model it actually opens. Allow view or change permission, including permissions granted through groups; active staff superusers see every option. Dashboard is the common staff entry point. Sidebar filtering does not replace page or dashboard-data permission checks.
- Put dashboard data preparation in `dashboard/views.py`; check permissions before querying and displaying restricted data.
- Guard every dashboard card, chart, list, and its queries with the same model view/change permission used by navigation. Check add permissions separately for create buttons. Related patient or staff details need their own permissions. Test that denied data is absent from the context, HTML, chart JSON, and database queries; include a friendly empty state for staff without dashboard access.
- Escape user content. Use `format_html()` with substitution arguments, `format_html_join()`, or normal template escaping. Use `json_script` when passing data to JavaScript.
- Check list, search, add, edit, validation-error, and related-record screens after changes. Include a saved prescription with medicines when checking prescription screens.
- Check layout in light and dark mode when making visual admin changes. Keep custom JavaScript narrowly scoped and use Django static-file discovery.
- Preserve the single-clinic intent unless the requested feature changes it.
- Resetting another user's password requires `is_superuser`, checked on the server. The administrator role label alone is not enough. Keep permission fields protected so a staff editor cannot promote themselves to bypass this rule.
- Use Django's password forms, validation, hashing, and admin history for resets. Never store or log the entered password. Test denied direct requests, rejected passwords, successful login, and session invalidation.
- Verify that access-denied pages render correctly when testing permissions; a blocked request must return a working 403 page, not crash because of an obsolete URL.

## Do not

- Do not overwrite unrelated edits, reset the repository, or rewrite working features to match personal preferences.
- Do not revive old `PatientProfile`, patient-role users, accounting screens, or commented routes just because old documentation mentions them.
- Do not replace the admin theme, introduce a new frontend framework, or add dependencies without a clear need in the requested task.
- Do not treat a role name, `is_staff`, or a hidden menu item as proof of permission to view clinical data. Do not give everyone superuser access to solve permission problems.
- Do not put passwords, real patient details, database copies, or secrets in code, logs, screenshots, test fixtures, or commits. Use synthetic test records.
- Do not prefill production login passwords or run demo seed/reset commands against real clinic data.
- Do not delete patients, medicines, or staff without reviewing effects on historical records. Prefer deactivation where appropriate.
- Do not delete databases, fake migrations, or rewrite applied migration history as a shortcut. Do not change a foreign key's target without a verified record mapping.
- Do not copy the current one-to-one appointment relationships into new booking features. Appointment history needs multiple visits; one availability record per physician is a different rule.
- Do not rely only on JavaScript, dropdown filtering, or `limit_choices_to` to enforce a business rule. Do not assume ordinary `save()` calls validate every model.
- Do not use bulk updates for fields whose correctness depends on `save()` unless the operation explicitly handles those rules.
- Do not show a success message for a form that has not actually completed its promised action.
- Do not claim that all workflows work because `manage.py check` passes or the test runner reports zero tests.

## Before finishing a change

Run commands with the project's virtual environment. On Windows, replace `python` below with `.\venv\Scripts\python.exe` if the environment is not activated.

| Change | Appropriate checks |
| --- | --- |
| Python/model/admin logic | `python manage.py check` and focused tests for the affected behavior. |
| Model fields or relationships | `python manage.py makemigrations --check --dry-run`, plus fresh and upgrade migration checks using a disposable test database. |
| Permissions | Test a superuser, allowed staff, denied staff, and anonymous access where relevant. Check direct URLs and dashboard contents. |
| Admin UI | Exercise affected screens with empty and populated records, including invalid form submissions. |
| Deployment/settings | `python manage.py check --deploy --settings=core.settings.production`; verify actual deployment configuration. |
| Formatting | Run the configured pre-commit checks on changed files and inspect any edits they make. |
| Documentation only | Verify claims, paths, and Markdown. No new application tests are needed. |

Use `python manage.py test` for the project suite when relevant. Password-reset regression tests are in `accounts/tests/test_admin_password_reset.py`; other workflows still need coverage. Add meaningful regression tests when fixing behavior; do not change unrelated code just to make a check pass.

Name Django test files `test_*.py`. Keep the pre-commit test-name hook in Django mode so it agrees with Django's test discovery.

Never run migrations, seeding, or destructive experiments on the existing clinic database as a routine verification step. Use a disposable database and synthetic records. State clearly when a check could not be run.
