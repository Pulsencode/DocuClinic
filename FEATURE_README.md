# DocuClinic Feature Reference

## Overview

DocuClinic is a Django-based clinic management system. Data and workflows are currently handled through the Django admin interface (django-unfold) at `/admin/`. Models and admin screens exist for the main clinic domains; custom staff and patient pages are not yet wired up.

---

## Current Features

Everything below is available today through the admin panel unless noted otherwise.

### User Management

- Custom `User` model extending Django auth
- User roles:
  - Administrator
  - Physician
  - Nurse
  - Receptionist
  - Accountant
  - Patient
- Auto-generated registration IDs with role prefixes (ADM, PHY, NUR, REC, ACC, PAT)
- User fields: username, name, email, phone, address, active/staff flags
- Admin login and logout for staff
- Patient profile shown inline when editing a patient user in admin
- Admin list/search/filter for users and patient profiles

### Patient Management

- `PatientProfile` linked one-to-one with a patient user
- Personal details: age, gender, blood type
- Vital signs: height, weight, temperature, temperature method, pulse, blood pressure
- Automatic BMI calculation and BMI status (Underweight, Normal, Overweight, Obese)
- Allergies and emergency contact name/number
- VIP patient flag
- Admin CRUD for patient profiles

### Appointments

- `Appointment` model linking patient and physician users
- Fields: date, time, status, consultation fee, discount, created timestamp
- Status options: Scheduled, Pending, Completed, Cancelled
- `PhysicianAvailability` model: work days, start/end times, lunch break
- `Weekday` model for scheduling days (Monday through Sunday)
- Admin CRUD with search, filters, and autocomplete for patient/physician/discount

### Medical Records

- `Prescription` model: diagnosis, notes, prescription date, follow-up date
- `PrescriptionMedicine` model: medicine, dose, frequency, timing, amount, instructions
- `Discount` model: percentage value with timestamps
- Discount can be applied to appointments
- Admin CRUD for prescriptions, prescription medicines, and discounts

**Note:** Prescriptions are not yet linked to a patient or physician in the database model.

### Inventory

- `Medicine` model: name, generic name, brand name, route of administration, description, quantity, expiration date, purchase date, min/max stock levels, storage location
- `is_expired()` helper on medicine records
- `Supplier` model: name, contact details, email, address
- `RouteOfAdministration` model (e.g. oral, injection)
- `MedicineSupplier` through model: price and supply date per medicine-supplier pair
- Admin CRUD for all inventory models

### Accounting

- `Account` model with types: Asset, Liability, Expense, Revenue, Equity
- `GeneralLedgerEntry` model: date, description, debit account, credit account, amount
- `AccountsReceivable` model: name, amount, due date, description, status (Pending, Paid, Overdue)
- `AccountsPayable` model: same structure as receivable
- `Invoice` model: invoice number, organization name, date, total amount, optional receivable link
- `Asset` model: purchase date/value, current value, depreciation rate
- Admin CRUD for all accounting models

### Clinic Settings

- Single `Clinic` instance allowed (enforced in model validation and admin)
- Fields: name, address, email, contact number, GST number, license number, logo, consultation duration
- Admin create/update for clinic settings

### Admin Interface

- django-unfold themed admin with grouped sidebar navigation
- Sections: Clinic, Users and Patients, Appointments, Medical Records, Inventory, Accounting
- Search and filters on key list views
- Static media serving configured for development

### Development and Deployment

- SQLite database by default (MySQL config available but commented out)
- Environment variables via `.env`
- Docker and Docker Compose support
- `seed_demo_data` management command (needs model updates before it works)
- GitHub Actions CI running tests
- Pre-commit hooks with Flake8

### Legacy Code (Not Active)

The following exist in the repository but are commented out or have empty URL configs:

- Custom list/create/update/delete views for patients, physicians, appointments, prescriptions, inventory, accounting, and clinic
- Role-specific dashboard templates (admin, physician, nurse, receptionist, accountant)
- Bootstrap-based frontend templates and forms
- Custom signup and login pages beyond Django admin

---

## First Version Features Needed

These are the features required for a minimal first release (v1) that staff and patients can use outside of raw admin data entry. Items are grouped by priority area.

### 1. Staff Web Interface

- [ ] Connect existing views and URL routes (or rebuild a minimal set)
- [ ] Shared layout with navigation sidebar for staff pages
- [ ] Login page for staff with redirect after authentication
- [ ] Role-based access: restrict pages by user role

### 2. User and Role Setup

- [ ] Physician profile model or fields: specialization, license number, consultation fee
- [ ] Staff user creation flow (receptionist/admin creates physician, nurse, etc.)
- [ ] Role-based home page after login:
  - [ ] Administrator dashboard (appointment count, staff count, patient count)
  - [ ] Physician dashboard (today's appointments)
  - [ ] Receptionist dashboard (appointments to manage)
  - [ ] Nurse dashboard (patient vitals overview)
  - [ ] Accountant dashboard (pending invoices/payments)

### 3. Patient Registration and Profiles

- [ ] Patient self-registration or receptionist-led registration form
- [ ] Patient login (view own appointments and prescriptions only)
- [ ] Patient list page with search and pagination
- [ ] Patient detail page showing profile, vitals, and history

### 4. Appointments (Core Workflow)

- [ ] Appointment booking form (receptionist or patient)
- [ ] Change appointment model from OneToOne to ForeignKey so patients can have multiple appointments
- [ ] Validate date/time against physician availability and clinic consultation duration
- [ ] Block double-booking for the same physician slot
- [ ] Appointment list with filters (physician, status, date)
- [ ] Appointment detail and status update (Scheduled, Completed, Cancelled)
- [ ] Auto-calculate consultation fee from physician fee minus discount

### 5. Medical Records

- [ ] Add patient and physician foreign keys to `Prescription`
- [ ] Prescription create form linked to an appointment or patient visit
- [ ] Prescription detail page with medicine list
- [ ] Patient prescription history page
- [ ] Printable or PDF prescription output

### 6. Inventory (Basic)

- [ ] Medicine list page with search and filters
- [ ] Low-stock warning when quantity is below minimum level
- [ ] Expired medicine flag on list view
- [ ] Supplier and route-of-administration management pages

### 7. Accounting (Basic)

- [ ] Record payment when appointment is marked Completed
- [ ] Create invoice or accounts receivable entry from appointment fee
- [ ] Simple daily revenue summary (appointments completed and amount collected)
- [ ] Accounts list and basic ledger entry form

### 8. Clinic Setup

- [ ] Clinic settings page (or ensure admin setup is documented as the v1 approach)
- [ ] Display clinic name and logo on staff pages and printed prescriptions

### 9. Data and Quality

- [ ] Fix `seed_demo_data` to work with the current `User` and `PatientProfile` models
- [ ] Basic test coverage for appointment booking and prescription creation
- [ ] Error pages (404, 403) wired if custom frontend is enabled

### 10. Out of Scope for v1

The following can wait until after the first release:

- SMS or email notifications
- Patient document uploads
- Lab results and imaging
- Payment gateway integration
- Advanced financial reports (balance sheet, income statement)
- Multi-clinic or branch support
- Mobile app
- API for third-party integrations
- HIPAA compliance tooling beyond standard Django security

---

## Suggested v1 User Flows

### Receptionist
1. Log in
2. Register a new patient or find an existing one
3. Book an appointment with an available physician
4. Mark appointment as Completed and record payment

### Physician
1. Log in
2. View today's appointments
3. Open patient profile and vitals
4. Create a prescription with medicines
5. Print or save prescription for the patient

### Patient
1. Register or log in
2. View upcoming appointments
3. View past prescriptions

### Administrator
1. Log in
2. View clinic dashboard summary
3. Manage staff users, clinic settings, and discounts
4. Review inventory and accounting entries
