import json
from unittest import TestCase

from companies.models import Company
from django.test import Client
from django.urls import reverse
import pytest


@pytest.mark.django_db
class BasicCompanyAPITestCase(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.companies_url = reverse("companies-list")

    def tearDown(self) -> None:
        pass


class TestGetCompanies(BasicCompanyAPITestCase):

    def test_zero_companies_should_return_empty_list(self) -> None:

        response = self.client.get(self.companies_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), [])

    def test_one_company_exists_should_succedd(self) -> None:

        test_company = Company.objects.create(name="amazon")
        response = self.client.get(self.companies_url)
        response_content = json.loads(response.content)[0]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_content.get("name"), test_company.name)
        self.assertEqual(response_content.get("status"), "Hiring")
        self.assertEqual(response_content.get("application_link"), "")
        self.assertEqual(response_content.get("notes"), "")

        test_company.delete()

class TestPostCompanies(BasicCompanyAPITestCase):
    def test_create_company_without_arguments_should_fail(self) -> None:
        response = self.client.post(path=self.companies_url)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            json.loads(response.content), {"name": ["This field is required."]}
        )

    def test_create_existing_company_should_fail(self) -> None:
        Company.objects.create(name="Google")
        response = self.client.post(path=self.companies_url, data={"name":"Google"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            json.loads(response.content),
            {"name": ["company with this name already exists."]}
        )

    def test_create_company_with_only_name_all_fields_should_be_default(self) -> None:
        response = self.client.post(path=self.companies_url, data={"name": "teste name"})
        self.assertEqual(response.status_code, 201)
        response_content = json.loads(response.content)
        self.assertEqual(response_content.get("name"), "teste name")
        self.assertEqual(response_content.get("status"), "Hiring")
        self.assertEqual(response_content.get("application_link"), "")
        self.assertEqual(response_content.get("notes"), "")

    def test_create_company_with_layoffs_status_should_succeed(self) -> None:

        response = self.client.post(path=self.companies_url, data={"name": "teste name", "status":"layoffs"})
        self.assertEqual(response.status_code, 201)
        response_content = json.loads(response.content)
        self.assertEqual(response_content.get("name"), "teste name")
        self.assertEqual(response_content.get("status"), "layoffs")
        self.assertEqual(response_content.get("application_link"), "")
        self.assertEqual(response_content.get("notes"), "")

    def test_create_company_with_wrong_status_should_fail(self) -> None:
        response = self.client.post(path=self.companies_url, data={"name": "teste name", "status":"Wrong"})
        self.assertEqual(response.status_code, 400)
        self.assertIn("Wrong", str(response.content))
        self.assertIn("is not a valid choice", str(response.content))