from datetime import date, time

from django.db import connection
from django.db.migrations.executor import MigrationExecutor
from django.test import TransactionTestCase


class CalendarMigrationTests(TransactionTestCase):
    def test_upgrade_preserves_links_and_allows_repeated_visits(self):
        executor = MigrationExecutor(connection)
        before = [("appointments", "0003_alter_appointment_patient")]
        after = [("appointments", "0004_calendar_booking")]
        executor.migrate(before)
        try:
            apps = executor.loader.project_state(
                before + [("clinic", "0001_initial")]
            ).apps
            doctor = apps.get_model("accounts", "User").objects.create(
                username="migration_doctor",
                role="physician",
                registration_id="PHY-SYNTHETIC",
            )
            patient = apps.get_model("accounts", "Patient").objects.create(
                first_name="Migration", registration_id="PAT-SYNTHETIC"
            )
            apps.get_model("clinic", "Clinic").objects.create(
                name="Synthetic", consultation_duration=30
            )
            old = apps.get_model("appointments", "Appointment").objects.create(
                physician_id=doctor.pk,
                patient_id=patient.pk,
                date=date(2030, 1, 1),
                time=time(9),
                consultation_fee=123,
            )
            executor = MigrationExecutor(connection)
            executor.migrate(after)
            model = executor.loader.project_state(after).apps.get_model(
                "appointments", "Appointment"
            )
            saved = model.objects.get(pk=old.pk)
            self.assertEqual(
                (
                    saved.patient_id,
                    saved.physician_id,
                    saved.consultation_fee,
                    saved.duration_minutes,
                ),
                (patient.pk, doctor.pk, 123, 30),
            )
            model.objects.create(
                physician_id=doctor.pk,
                patient_id=patient.pk,
                date=date(2030, 1, 2),
                time=time(9),
            )
            self.assertEqual(model.objects.count(), 2)
        finally:
            MigrationExecutor(connection).migrate(after)
