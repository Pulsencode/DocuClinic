# DocuClinic project review

Reviewed: 20 September 2026.

The project has a useful Django admin foundation, but parts of the patient redesign have not been carried through to the dashboard and appointments. Fix these broken paths and access controls before adding more features.

This review covers the current working files, including existing uncommitted changes. It does not change application code or the existing database. Runtime examples used synthetic records in a separate, in-memory database. This is a code review, not a complete production or clinical assessment.

## 1. How the project works today

| Area | Current approach |
| --- | --- |
| Framework | Django 6.0.3 with django-unfold 0.84.0. The local environment uses Python 3.14.5. |
| Structure | One Django application split into domain apps: accounts, appointments, medical records, inventory, clinic, dashboard, and public interface. |
| Main interface | Staff use Django admin at `/management/`. `/` is a public landing page. |
| Data | Django models and ORM queries, with SQLite configured for development and production. MySQL examples are commented out. |
| Staff and patients | `User` extends Django's `AbstractUser` for staff. `Patient` is a separate model without login credentials. Staff roles are administrator, physician, nurse, and receptionist. |
| Business logic | Small model methods calculate BMI, age, registration IDs, and expiry. Some models implement `clean()` or `save()` validation. There is no separate service layer. |
| Relationships | Prescriptions already link to patients and physicians. Prescription medicines are child records. Medicine suppliers use an intermediate model for price and supply date. |
| Rendering | Django templates and server-rendered admin forms. The dashboard uses local ApexCharts JavaScript. The public page loads Tailwind and fonts externally. |
| Settings | Shared settings in `core/settings/base.py`; development and production override them. `manage.py` defaults to development; WSGI and ASGI default to production. |
| Older code | Most custom forms and views outside the admin are commented out; their app URL lists are empty. Those templates are not active workflows. |
| Accounting | No accounting app is present. Its settings and navigation entries are commented out. |

The coding style is conventional Django: model classes, decorated admin registrations, named URLs, and small helper methods. Business rules and presentation are mostly separated, but validation is inconsistent and old field references remain after model changes.

## 2. How the admin is configured

| File | Responsibility |
| --- | --- |
| `core/urls.py` | Mounts Django's default admin site at `/management/`. |
| `core/settings/base.py` | Loads `unfold` before `django.contrib.admin`, allowing the theme to supply admin templates. |
| `core/settings/unfold.py` | Sets branding, sidebar groups, named navigation links, the dashboard callback, and time-shortcut JavaScript. |
| Each app's `admin.py` | Registers models and controls columns, search, filters, fields, autocomplete, and inline records. |
| `accounts/admin.py` | Combines Django's `UserAdmin` with Unfold; provides detailed patient forms and read-only calculated values. |
| `medicalrecords/admin.py` | Adds prescription medicines inline, tabs, summaries, and related-record query optimization. |
| `clinic/admin.py` | Redirects the clinic list to the existing clinic's edit page or the add page. |
| `dashboard/views.py` | Builds dashboard counts, alerts, charts, appointments, and follow-ups. |
| `templates/admin/` | Overrides dashboard, login, branding, and menu templates. |
| `appointments/static/js/custom_time_shortcuts.js` | Changes the available hour shortcuts; it does not validate appointment availability. |

Good patterns to keep:

- Unfold `ModelAdmin` and `TabularInline` keep the main interface consistent.
- User, patient, and prescription screens use useful search fields and grouped forms.
- Registration IDs, BMI, and system timestamps are read-only where appropriate.
- Prescription lists use `select_related()` and a medicine-count annotation to avoid repeated database queries.
- Most custom HTML uses Django's escaping helpers.
- The seeder uses a database transaction and Django password hashing.

Admin coverage is uneven: inventory screens are mostly default forms, while patient and prescription screens are more complete. The sidebar item named **Suppliers** opens medicine-supplier pricing records, not the supplier directory.

Access currently depends on Django's staff flag, groups, and permissions. A role label alone does not grant model permissions or restrict records to a physician. The demo seeder marks staff accounts as staff but does not assign their groups or model permissions.

## 3. Findings and recommended actions

**First** means a confirmed broken workflow, exposure, or risk of incorrect record linkage. **Next** means missing behavior or protection to address before normal clinic use. **Later** means maintenance and consistency work.

### Fix first

| Finding | Evidence and effect | Recommended action |
| --- | --- | --- |
| Dashboard exposes diagnosis data without the relevant permission. | `dashboard/views.py:28` does not check permissions before querying records, and `templates/admin/index.html` displays them. A synthetic staff user with no prescription view permission received HTTP 200 and saw a follow-up diagnosis. | Check permissions before querying and rendering each section. Define which records each staff role may see, and test direct access as well as menus. |
| Old patient fields break active pages. | `appointments/models.py:43` reads `patient.username`; `appointments/admin.py:27` searches `patient__username`; `templates/admin/index.html:163` expects patient user methods/fields. `Patient` has none of these. Reproduced string conversion and search errors; the dashboard fails when today's appointments are present. | Use actual `Patient` name and registration fields. Check all references together when changing a model. |
| Dashboard patient count and add button are wrong. | `dashboard/views.py:77` counts patient-role users; one actual patient produced a count of zero. `templates/admin/index.html:29` sends Add Patient to the user form. The VIP count is referenced but not supplied. | Count `Patient` records, link to the patient add form, and supply the VIP count. |
| Prescription medicine summary crashes. | `medicalrecords/admin.py:334` calls `format_html()` without substitution arguments. Reproduced `TypeError` when a prescription has medicines. | Combine escaped items with `format_html_join()` or a template, then test a saved prescription containing medicines. |
| Appointment relationships permit only one appointment per patient and per physician. | Both fields in `appointments/models.py:17` and `:22` are `OneToOneField`. This is a lifetime uniqueness restriction, not a time-slot restriction. | Use many-to-one relationships for appointment history, with explicit scheduling rules and a safe migration. Keep the separate one-to-one physician availability record if that design remains intended. |
| The patient relationship migration does not map existing records. | `appointments/migrations/0002_alter_appointment_patient.py` changes the target from `User` to `Patient` with only `AlterField`. Numeric IDs from these tables are not equivalent identities. | Before applying to a populated older database, define and verify a patient mapping. Otherwise migration can fail or attach appointments to the wrong patient. Fresh empty-database migration success does not prove upgrade safety. |
| Login includes hardcoded demo credentials. | `templates/admin/login.html` fills the username and password using JavaScript. The seeder also creates a demo superuser and resets demo passwords on reruns. No production guard is present. | Remove automatic credential filling from normal login. Restrict demo setup to disposable demo environments. This review did not try those credentials against existing accounts. |

### Address next

| Finding | Evidence and effect | Recommended action |
| --- | --- | --- |
| Scheduling rules are not enforced. | Availability and consultation duration are stored, but active appointment code does not check working hours, lunch, duration, or slot conflicts. | Add shared server-side validation, then protect booking against simultaneous conflicting requests. Specify cancellation behavior before designing slot constraints. |
| Prescription validation can crash on incomplete input. | `medicalrecords/models.py:40` accesses `self.physician.role` even when no physician is set. A synthetic `full_clean()` call raised `RelatedObjectDoesNotExist`. | Let missing fields produce normal form errors; guard related-object access. Test missing, wrong-role, and inactive physicians. |
| Numeric and date rules are incomplete. | Discount percentage has no 0–100 validator; stock thresholds can be negative or reversed; future birth dates and invalid measurements are not rejected by custom rules. | Define valid inputs and enforce them in models/forms, with database constraints where appropriate. Do not invent clinical thresholds without requirements. |
| Deletion can erase history. | Patient deletion cascades to appointments and prescriptions. Medicine deletion cascades to prescription medicine rows. Physician deletion is protected for prescriptions but cascades for appointments. | Agree on record retention, prefer deactivation, and protect historical references as required. Review existing delete permissions and bulk actions. |
| Production setup needs work. | `check --deploy` reported missing HSTS, HTTPS redirect, secure session and CSRF cookies, and a weak secret in the local environment. Static/media URLs use Django's development file-serving view unconditionally. `django_lumen` is installed through shared settings. | Configure deployment-specific security and file serving; keep database visualization tooling development-only. The live hosting/proxy setup was not inspected. |
| Docker startup is incomplete. | `Dockerfile` runs Gunicorn, but `requirements.txt` does not include it. Compose defines no environment injection or persistent database/media volumes. `.dockerignore` does not exclude `venv/`, `db.sqlite3`, logs, or uploaded media. | Complete and verify container startup, configuration, and persistence. Exclude local data and environments from the image. Docker was not built during this review. |
| There are no executable project tests. | `manage.py test --noinput` found zero tests; existing test files are placeholders or commented out. CI runs this same command. | Add tests for permissions, patient and appointment admin paths, prescription validation and rendering, and safe data migrations. A green CI run currently provides little workflow assurance. |
| Clinic singleton is only partly enforced. | `clinic/models.py:19` checks for an existing clinic in `clean()`, and admin redirects to one record. Ordinary model saves do not invoke that check automatically; there is no database singleton constraint. | Preserve the one-clinic design across admin, commands, and concurrent writes if it is a firm requirement. |
| Registration ID generation can collide under concurrent requests. | User and patient generators check whether a random ID exists before saving. Another request can choose the same ID between those operations. The unique field rejects duplicates, but there is no retry. | Handle uniqueness conflicts safely or choose a suitable database-backed sequence. |

### Improve later

- **Documentation is stale.** `README.md` and `FEATURE_README.md` describe `/admin/`, patient login users, `PatientProfile`, accounting, missing prescription links, and `seed_demo_data`. Current code uses `/management/`, separate `Patient` records, existing prescription links, and `seed_accounts_data`.
- **The public demo form only simulates success.** Its JavaScript prevents submission and shows “Request Sent”; the server does not store or email the request. Label it as a demo or implement a real submission flow.
- **Formatting configuration is unclear.** Pre-commit runs Black, isort, and Flake8. `core.toml` is not explicitly passed to those hooks and contains an old Python 3.8 target. Flake8 allows 150 characters while the formatter configuration says 88. Align the configuration and document one routine.
- **Validation is inconsistent across write paths.** `Prescription.save()` calls `full_clean()`, while most other saves do not. Bulk ORM updates bypass model save methods, including BMI recalculation and ID generation. Document and test the intended write paths.
- **Environment values need explicit types.** Base settings read booleans such as `EMAIL_USE_TLS` as strings. Development and production explicitly override `DEBUG`, so its base string value is not the active debug setting in those profiles.
- **Some dependencies look left over.** Semantic admin/forms and other packages are pinned but not configured as active apps. Confirm actual usage before removing them; do not upgrade or replace the current theme as part of cleanup.

## 4. Verification performed

| Check | Result |
| --- | --- |
| Django system check | Passed. |
| Migration drift: `makemigrations --check --dry-run` | No changes detected, including the existing untracked migrations. |
| Local migration plan | All listed migrations already marked applied; no migrations applied to the existing database by this review. |
| Project test command | Zero tests discovered. |
| Fresh migrations in an in-memory database | Passed. |
| Synthetic appointment and prescription probes | Reproduced the field lookup, rendering, summary, and incomplete-physician errors listed above. |
| Synthetic staff permission probe | Confirmed a follow-up diagnosis is visible without prescription view permission. |
| Public homepage via Django test client | HTTP 200. |
| Production settings check | Five security warnings in the current local environment. |

No browser visual review, Docker build, real-data upgrade simulation, concurrency load test, or full dependency vulnerability audit was performed. File references describe the reviewed snapshot and may move as code changes.

## 5. Suggested order of work

1. Restrict dashboard data by permission and remove demo login defaults.
2. Fix patient references, dashboard counts/links, and prescription rendering/validation.
3. Correct appointment relationships with a data-preserving migration and scheduling rules.
4. Add regression tests for these workflows, then review deletion and validation rules.
5. Finish deployment configuration and update the existing feature/setup documentation.

The companion `AGENTS.md` is the simple rule book for future AI-assisted work. Its rules describe how changes should be made; they do not mean the findings above have already been fixed.
