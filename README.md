<h1 align="center">DocuClinic</h1>

![Python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)
![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-00000F?style=for-the-badge&logo=mysql&logoColor=white)
![ChartJS](https://img.shields.io/badge/Chart%20js-FF6384?style=for-the-badge&logo=chartdotjs&logoColor=white)
![JQuery](https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white)
![NGINX](https://img.shields.io/badge/Nginx-009639?style=for-the-badge&logo=nginx&logoColor=white)
![Debian](https://img.shields.io/badge/Debian-A81D33?style=for-the-badge&logo=debian&logoColor=white)
![Warp](https://img.shields.io/badge/warp-01A4FF?style=for-the-badge&logo=warp&logoColor=white)


## Overview:
Web app for Clinic Management - A comprehensive Django-based clinic management system for managing patients, appointments, medical records, inventory, and accounting.

## Features

### User Management & Authentication
- User authentication system with login/logout
- Role-based access control with multiple user types:
  - **Administrator**: Full system access and management
  - **Physician**: Medical staff with appointment and prescription management
  - **Nurse**: Clinical support staff
  - **Receptionist**: Front desk operations
  - **Accountant**: Financial management
  - **Patient**: Patient portal access
- Automatic registration ID generation for each user type (ADM, PHY, NUR, RES, ACC, PAT prefixes)
- User profile management with detailed information
- Group and permission management system
- Role-specific dashboards

### Patient Management
- Patient registration and profile management
- Patient detail tracking including:
  - Personal information (age, gender, address, phone)
  - Medical information (blood type, allergies, emergency contacts)
  - Vital signs tracking (temperature, pulse, blood pressure, BMI)
  - Height and weight tracking with automatic BMI calculation
  - BMI status determination (Underweight, Normal, Overweight, Obese)
- VIP patient status flagging
- Patient list view with pagination
- Patient search and filtering capabilities
- Patient profile view with medical history

### Physician Management
- Physician registration with specialization and license number
- Fee per consultation configuration
- Physician availability management:
  - Work days scheduling (Monday-Sunday)
  - Work time slots (start and end times)
  - Lunch break scheduling
- Physician list view with details
- Physician dashboard showing assigned appointments
- Physician profile management

### Appointment Management
- Appointment scheduling system
- Appointment status tracking (Scheduled, Pending, Completed, Cancelled)
- Dynamic available date/time slot calculation based on:
  - Physician availability
  - Existing appointments
  - Consultation duration
  - Lunch break exclusions
- Appointment filtering by:
  - Physician
  - Status
  - Date range
- VIP patient discount application
- Consultation fee calculation with discount support
- Appointment detail view
- Appointment creation, update, and deletion

### Medical Records & Prescriptions
- Prescription creation and management
- Prescription detail tracking:
  - Diagnosis information
  - Prescription notes
  - Follow-up date scheduling
- Prescription medicine management:
  - Medicine selection
  - Dosage specification
  - Frequency and timing instructions
  - Additional instructions
- Patient prescription history view
- Prescription list with filtering
- Prescription detail view
- Prescription deletion capability

### Inventory Management
- Medicine inventory tracking:
  - Medicine details (name, generic name, brand name)
  - Route of administration
  - Quantity tracking
  - Expiration date monitoring
  - Purchase date tracking
  - Minimum and maximum stock levels
  - Storage location tracking
  - Expiration status checking
- Supplier management:
  - Supplier information (name, contact, email, address)
  - Supplier list, create, update, delete operations
- Route of administration management (oral, injection, etc.)
- Medicine-supplier relationship tracking:
  - Price per supplier
  - Supply date tracking
- Inventory dashboard with statistics
- Low stock alerts (based on minimum stock level)

### Accounting & Financial Management
- Account management:
  - Account types (Asset, Liability, Expense, Revenue, Equity)
  - Account list view
- General ledger entry system:
  - Debit and credit account tracking
  - Transaction date and description
  - Amount tracking
- Accounts Receivable management:
  - Customer payment tracking
  - Due date monitoring
  - Status tracking (Pending, Paid, Overdue)
- Accounts Payable management:
  - Vendor payment tracking
  - Due date monitoring
  - Status tracking (Pending, Paid, Overdue)
- Invoice management:
  - Invoice number generation
  - Organization name tracking
  - Date and total amount tracking
- Asset management:
  - Asset purchase tracking
  - Current value tracking
  - Depreciation rate calculation

### Clinic Management
- Clinic profile management:
  - Clinic name, address, contact information
  - Email and contact number
  - GST number
  - License number
  - Clinic logo upload
  - Consultation duration configuration
- Clinic detail view
- Clinic create, update, delete operations

### Discount Management
- Discount percentage configuration
- Discount application to appointments
- Discount creation, update, and deletion
- Automatic consultation fee calculation with discounts

### Dashboard & Analytics
- **Administrator Dashboard**:
  - Today's appointment count
  - Total staff counts (physicians, nurses, accountants, receptionists)
  - Total patient count
  - 7-day appointment trend chart
- **Physician Dashboard**:
  - Personal appointment list
  - Appointment filtering by date
- **Nurse Dashboard**: Clinical support overview
- **Receptionist Dashboard**: Front desk operations overview
- **Accountant Dashboard**: Financial overview
- **Inventory Dashboard**:
  - Total medicines count
  - Total suppliers count
  - Medicine-supplier relationship count

### Additional Features
- Pagination support across list views
- Search and filter capabilities
- Responsive Bootstrap-based UI
- Form validation and error handling
- Success/error message notifications
- User-friendly navigation with sidebar
- 404 and 403 error page handling
- Favicon support

## Features to be Added

### Patient Features
- [ ] Patient appointment booking portal
- [ ] Patient medical history timeline
- [ ] Patient document upload (lab reports, scans, etc.)
- [ ] Patient appointment reminders (SMS/Email)
- [ ] Patient prescription refill requests
- [ ] Patient payment history
- [ ] Patient insurance information management
- [ ] Patient family member linking

### Appointment Features
- [ ] Appointment reminder notifications (SMS/Email)
- [ ] Appointment rescheduling functionality
- [ ] Waitlist management for fully booked slots
- [ ] Recurring appointment scheduling
- [ ] Appointment cancellation reasons tracking
- [ ] No-show tracking and reporting
- [ ] Appointment confirmation system
- [ ] Calendar view for appointments
- [ ] Appointment conflict detection

### Medical Records Features
- [ ] Lab test results management
- [ ] Medical imaging reports (X-ray, MRI, CT scan)
- [ ] Diagnosis code management (ICD-10)
- [ ] Treatment plan templates
- [ ] Medical history search and filtering
- [ ] Prescription templates
- [ ] Drug interaction checking
- [ ] Allergy checking before prescription
- [ ] Medical report generation (PDF)
- [ ] Discharge summary generation

### Inventory Features
- [ ] Automated reorder alerts
- [ ] Purchase order management
- [ ] Stock movement tracking (in/out)
- [ ] Batch/lot number tracking
- [ ] Expired medicine alerts
- [ ] Medicine usage analytics
- [ ] Supplier performance tracking
- [ ] Inventory valuation reports
- [ ] Barcode scanning support
- [ ] Inventory audit trail

### Accounting Features
- [ ] Payment processing integration
- [ ] Payment method tracking (Cash, Card, Online)
- [ ] Payment receipt generation
- [ ] Financial reports (Income Statement, Balance Sheet)
- [ ] Revenue analytics and charts
- [ ] Expense categorization
- [ ] Tax calculation and reporting
- [ ] Payment reminders for overdue accounts
- [ ] Multi-currency support
- [ ] Bank reconciliation
- [ ] Financial year management
- [ ] Budget planning and tracking

### Communication Features
- [ ] SMS notification system
- [ ] Email notification system
- [ ] In-app messaging system
- [ ] Appointment confirmation emails
- [ ] Prescription ready notifications
- [ ] Payment receipt emails
- [ ] Automated follow-up reminders

### Reporting & Analytics
- [ ] Patient visit reports
- [ ] Revenue reports by period
- [ ] Physician performance reports
- [ ] Medicine usage reports
- [ ] Appointment statistics
- [ ] Patient demographics reports
- [ ] Custom report builder
- [ ] Export reports to PDF/Excel
- [ ] Dashboard widgets customization

### Security & Compliance
- [ ] Two-factor authentication (2FA)
- [ ] Activity logging and audit trail
- [ ] HIPAA compliance features
- [ ] Data encryption at rest
- [ ] Role-based data access restrictions
- [ ] Session timeout management
- [ ] Password policy enforcement
- [ ] Login attempt tracking

### Integration Features
- [ ] Laboratory system integration
- [ ] Pharmacy system integration
- [ ] Payment gateway integration
- [ ] Insurance provider API integration
- [ ] Electronic Health Records (EHR) export
- [ ] HL7/FHIR compatibility
- [ ] API for third-party integrations

### Additional System Features
- [ ] Multi-clinic/branch support
- [ ] Backup and restore functionality
- [ ] Data import/export (CSV, Excel)
- [ ] System settings configuration
- [ ] Email server configuration
- [ ] SMS gateway configuration
- [ ] Document management system
- [ ] Task and reminder system
- [ ] Notes and annotations
- [ ] File attachment support
- [ ] Advanced search functionality
- [ ] Dark mode theme
- [ ] Multi-language support
- [ ] Mobile app (iOS/Android)
- [ ] Offline mode support

## Setting up environment

### Prerequisites

Before starting, ensure you have the following installed on your system:

- Python (preferably version 3.11.7 or above)
- Pip (Python package installer)
- Virtual environment (optional but recommended for creating isolated Python environments)

**Create a Virtual Environment**

> [!CAUTION]
> Not creating a virtual environment can lead to project instability.

Creating a virtual environment helps isolate your project dependencies from other Python projects on your system. To create a virtual environment, run the following commands in your terminal:

1. Create a virtual environment named 'venv'
    ```bash
    python -m venv venv
    ```
2. Activating the environment

- For windows
    ```bash
    venv\Scripts\activate
    ```
- For macOS and Linux
    ```bash
    source venv/bin/activate
    ```

**Installing all the required libraries**

Now that you have a virtual environment set up, you can install Django and other libraries required within the project:

```bash
pip install -r requirements.txt
```

**Setting up mysql database server**

1. Download and install xampp for windows
2. Run the apache and mysql services
3. Open the admin panel for mysql
4. Create a data base named  ***pulse_flow***
5. Import the sql file to the database

**Running the project in your local system**

Before running ensure that the :
1. Virtual Environment is activated
2. Mysql is up and running

Run Migrations

```bash
python manage.py migrate
```

Then a super user has to be created
```bash
python manage.py createsuperuser
```

Then run the program in the development server
```bash
python manage.py runserver
```

**Development Requirements**
1. Needed Extensions
    1.1. Flake8
    1.2. mypy

2. Running pre commit before a commit

Only Clean when needed

```bash
pre-commit install
```

```bash
pre-commit run --all-files
```

```bash
pre-commit clean
```

## Run Test

```bash
python manage.py test
```

**Generate Fake Data For the Models**
Documentation of the library
- https://pypi.org/project/dj-data-generator/
```bash
python manage.py generate_data --num-records=1000
```
