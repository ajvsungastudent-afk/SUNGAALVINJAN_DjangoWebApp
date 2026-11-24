from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.urls import reverse

from .models import Student


class StudentAdminTests(TestCase):
    def setUp(self):
        self.staff = get_user_model().objects.create_user(
            username="records-staff",
            password="test-password",
            is_staff=True,
        )
        self.staff.user_permissions.set(
            Permission.objects.filter(
                content_type__app_label="registration",
                codename__in=(
                    "view_student",
                    "add_student",
                    "change_student",
                ),
            )
        )
        self.student = Student.objects.create(
            student_name="Test Student",
            program="Computer Science",
            year_level=2,
            email="student@example.com",
        )
        self.client.force_login(self.staff)

    def test_staff_can_view_add_and_change_but_not_delete_students(self):
        changelist = self.client.get(reverse("admin:registration_student_changelist"))
        add_form = self.client.get(reverse("admin:registration_student_add"))
        change_form = self.client.get(
            reverse("admin:registration_student_change", args=[self.student.pk])
        )
        delete_page = self.client.get(
            reverse("admin:registration_student_delete", args=[self.student.pk])
        )

        self.assertEqual(changelist.status_code, 200)
        self.assertContains(changelist, self.student.student_name)
        self.assertEqual(add_form.status_code, 200)
        self.assertEqual(change_form.status_code, 200)
        self.assertEqual(delete_page.status_code, 403)

    def test_admin_rejects_invalid_student_email(self):
        response = self.client.post(
            reverse("admin:registration_student_add"),
            {
                "student_name": "Invalid Email Student",
                "program": "Computer Science",
                "year_level": 1,
                "email": "not-an-email",
                "_save": "Save",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Enter a valid email address.")
        self.assertFalse(
            Student.objects.filter(student_name="Invalid Email Student").exists()
        )


class StudentApiTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="api-user",
            password="test-password",
        )
        self.student = Student.objects.create(
            student_name="API Test Student",
            program="Computer Science",
            year_level=2,
            email="api-student@example.com",
        )

    def test_student_api_requires_authentication(self):
        response = self.client.get(reverse("api_student_list"))

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"error": "Authentication required."})

    def test_authenticated_student_api_returns_database_records(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse("api_student_list"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "count": 1,
            "students": [{
                "id": self.student.pk,
                "student_name": "API Test Student",
                "program": "Computer Science",
                "year_level": 2,
                "email": "api-student@example.com",
            }],
        })
