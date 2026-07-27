# DocuClinic

A Django-based clinic management system. The application is currently managed through the Django admin interface (django-unfold).

## Overview

DocuClinic helps a clinic manage users, patients, appointments, prescriptions, medicine inventory, basic accounting, and clinic settings. Staff access the system through the admin panel at `/admin/`.

## Current Features

### User Management
- Custom user model with roles: Administrator, Physician, Nurse, Receptionist, Accountant, Patient
- Auto-generated registration IDs (ADM, PHY, NUR, REC, ACC, PAT prefixes)
- User contact details (phone, address)
- Django admin login for staff

### Patient Management
- Patient profile linked to user account
- Personal details: age, gender, blood type
- Vital signs: height, weight, BMI (auto-calculated), temperature, pulse, blood pressure
- Allergies and emergency contact information
- VIP patient flag

### Appointments
- Schedule appointments between patients and physicians
- Status tracking: Scheduled, Pending, Completed, Cancelled
- Consultation fee and discount support
- Physician availability (work days, hours, lunch break)

### Medical Records
- Prescription records with diagnosis, notes, and follow-up date
- Prescription medicines (dose, frequency, timing, instructions)
- Discount percentage configuration

### Inventory
- Medicine stock tracking (quantity, expiry, purchase date, storage location)
- Minimum and maximum stock levels
- Suppliers and routes of administration (oral, injection, etc.)
- Medicine-supplier pricing and supply dates

### Accounting
- Chart of accounts (Asset, Liability, Expense, Revenue, Equity)
- General ledger entries (debit/credit)
- Accounts receivable and accounts payable with status tracking
- Invoices and asset records

### Clinic Settings
- Single clinic profile (name, address, contact, GST, license)
- Clinic logo upload
- Consultation duration setting

## Basic Features Still Needed

These are the core items needed to make a simple, usable version of the app beyond admin-only data entry:

### Core Workflow
- Staff-facing web pages (the existing views and templates are not connected to URLs)
- Link prescriptions to patients and physicians (currently missing from the model)
- Physician profile fields (specialization, license number, consultation fee)
- Appointment slot validation based on physician availability
- One appointment per patient limitation should be reviewed (current model uses OneToOne)

### Users and Access
- Patient registration and login outside the admin panel
- Role-based dashboards (templates exist but are not active)
- Redirect staff to the correct dashboard after login

### Clinic Operations
- Record payment when an appointment is completed
- Connect appointment fees to invoices or accounts receivable
- Low-stock and expired medicine alerts
- Printable or downloadable prescription

### Data and Setup
- Update the demo data seeder to match the current user model (`seed_demo_data` command references removed models)
- Basic reports: daily appointments, patient count, revenue summary

## Tech Stack

- Python 3.12+
- Django 6
- django-unfold (admin UI)
- SQLite (default for local development)
- Pillow (image uploads)
- Docker (optional)

## Setup

### Prerequisites

- Python 3.12 or newer
- pip
- A virtual environment (recommended)

### Installation

1. Clone the repository and enter the project directory.

2. Create and activate a virtual environment.

   Windows:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

   macOS / Linux:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies.
   ```bash
   pip install -r requirements.txt
   ```

4. Copy the environment file and adjust values if needed.
   ```bash
   cp .env.example .env
   ```

5. Run migrations.
   ```bash
   python manage.py migrate
   ```

6. Create a superuser.
   ```bash
   python manage.py createsuperuser
   ```

7. Start the development server.
   ```bash
   python manage.py runserver
   ```

8. Open http://127.0.0.1:8000/admin/ and sign in with your superuser account.


### Optional: Docker

```bash
docker compose up --build
```

See `README.Docker.md` for more details.

### Optional: MySQL

MySQL settings are available in `core/settings/development.py` and `core/settings/production.py` but are commented out. SQLite is used by default. Uncomment the MySQL database block and set the values in `.env` if you want to use MySQL instead.

## Run Tests

```bash
python manage.py test
```

## Development

Install pre-commit hooks when needed:
```bash
pre-commit install
pre-commit run --all-files
```

Linting uses Flake8 (see `.flake8`).
