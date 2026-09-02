import uuid

from django.test import SimpleTestCase
from django.urls import reverse


class NormRouteTests(SimpleTestCase):
    def test_norm_details_reverse_accepts_uuid_pk(self):
        norm_id = uuid.uuid4()

        self.assertEqual(
            reverse('norm_proc_app:norm_details', kwargs={'norm_id': norm_id}),
            f'/norm_details/{norm_id}/',
        )
