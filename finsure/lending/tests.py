# Create a test to check a get a specific lender by id
import io
from random import random

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client
from rest_framework import status
from .models import Lender
import json
import csv

CONTENT_TYPE = "application/vnd.api+json"


class LenderTestCase(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def tearDown(self) -> None:
        Lender.objects.all().delete()

    def test_get_lender_by_id(self) -> None:
        lender = Lender.objects.create(
            name="Test Lender",
            code="TL001",
            upfront_commission_rate=0.5,
            trial_commission_rate=0.3,
            active=True,
        )
        response = self.client.get(f"/finsure/lenders/{lender.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content)["data"]
        attributes = response_data["attributes"]
        self.assertEqual(response_data["id"], str(lender.id))
        self.assertEqual(attributes["name"], lender.name)
        self.assertEqual(attributes["code"], lender.code)
        self.assertEqual(
            attributes["upfront_commission_rate"],
            lender.upfront_commission_rate,
        )
        self.assertEqual(
            attributes["trial_commission_rate"],
            lender.trial_commission_rate,
        )
        self.assertEqual(attributes["active"], lender.active)

    def test_post_new_lender(self) -> None:
        lender_data = {
            "name": "Test Lender 2",
            "code": "TL002",
            "upfront_commission_rate": 0.5,
            "trial_commission_rate": 0.3,
            "active": True,
        }
        response = self.client.post(f"/finsure/lenders/", lender_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_data = json.loads(response.content)["data"]
        attributes = response_data["attributes"]
        self.assertEqual(attributes["name"], lender_data["name"])

    def test_patch_lender(self) -> None:
        lender = self.add_new_lender()
        payload = {
            "data": {
                "type": "Lender",
                "id": f"{lender['id']}",
                "attributes": {
                    "name": "Lender 3",
                    "code": "123",
                    "upfront_commission_rate": 0.12,
                    "trial_commission_rate": 0.15,
                    "active": False,
                },
            }
        }

        response = self.client.patch(
            f"/finsure/lenders/{lender['id']}/", data=payload, content_type=CONTENT_TYPE
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content)["data"]
        response_attributes = response_data["attributes"]
        self.assertEqual(
            response_attributes["name"], payload["data"]["attributes"]["name"]
        )

    def test_upload_csv(self) -> None:
        csv_content = self.build_csv_string_sample()

        f = SimpleUploadedFile("lenders.csv", bytes(csv_content, "utf-8"))
        response = self.client.post(
            f"/finsure/lenders_upload/",
            {"file": f, "content_type": "multipart/form-data"},
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.get(f"/finsure/lenders/")
        self.assertEqual(len(json.loads(response.content)["data"]), 5)

    def build_csv_string_sample(self) -> str:
        sample_data = [self.new_lender_data(i) for i in range(0, 10)]
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=sample_data[0].keys())
        writer.writeheader()
        writer.writerows(sample_data)
        csv_content = output.getvalue()
        return csv_content

    def test_delete_lender(self):
        data = self.add_new_lender()
        response = self.client.delete(f"/finsure/lenders/{data['id']}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.client.get(f"/finsure/lenders/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(json.loads(response.content)["data"]), 0)

    def add_new_lender(self) -> dict:
        lender_data = self.new_lender_data()
        response = self.client.post(f"/finsure/lenders/", data=lender_data)
        return json.loads(response.content)["data"]

    @staticmethod
    def new_lender_data(num=0):
        lender_data = {
            "name": f"Test Lender {num}",
            "code": f"TL00{num}",
            "upfront_commission_rate": round(random(), 3),
            "trial_commission_rate": round(random(), 3),
            "active": True,
        }
        return lender_data

    def test_post_bad_data_400(self):
        lender_data = {
            "name": "Test Lender 2",
            "upfront_commission_rate": 0.5,
            "trial_commission_rate": 0.3,
            "active": True,
        }
        response = self.client.post(f"/finsure/lenders/", lender_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_lenders(self):
        for i in range(0, 8):
            self.add_new_lender()
        response = self.client.get(f"/finsure/lenders/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(json.loads(response.content)["data"]), 5)
        response = self.client.get(f"/finsure/lenders/?page_number=2")
        self.assertEqual(len(json.loads(response.content)["data"]), 3)
