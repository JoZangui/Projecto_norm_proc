import uuid

from django.contrib.auth import get_user_model
from django.test import SimpleTestCase, TestCase
from django.urls import reverse

from users_app.models import Department

from .models import Norms


class NormRouteTests(SimpleTestCase):
    def test_norm_details_reverse_accepts_uuid_pk(self):
        norm_id = uuid.uuid4()

        self.assertEqual(
            reverse('norm_proc_app:norm_details', kwargs={'norm_id': norm_id}),
            f'/norm_details/{norm_id}/',
        )


class SubmitNormForReviewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="editor@example.com",
            username="editor",
            password="password",
        )
        self.department = Department.objects.create(name="Operations", acronym="OPS")
        self.norm = Norms.objects.create(
            title="Norma de teste",
            document_type="policy",
            author=self.department,
            responsible_department=self.department,
            document_owner=self.department,
            drafted_by=self.user,
        )
        self.client.force_login(self.user)
        self.url = reverse(
            "norm_proc_app:submit_norm_for_review",
            kwargs={"norm_id": self.norm.pk},
        )

    def test_submit_changes_draft_to_under_review(self):
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "under_review"})
        self.norm.refresh_from_db()
        self.assertEqual(self.norm.status, "under_review")

    def test_submit_rejects_norm_that_is_not_draft(self):
        self.norm.status = "approved"
        self.norm.save(update_fields=["status"])

        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 400)
        self.norm.refresh_from_db()
        self.assertEqual(self.norm.status, "approved")

    def test_submit_requires_post(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 405)
