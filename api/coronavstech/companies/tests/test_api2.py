import json

from companies.models import Company
from django.urls import reverse
import pytest
companies_url = reverse("companies-list")
pytestmark = pytest.mark.django_db

#------- Test Get Companies --------------
def test_zero_companies_should_return_empty_list(client) -> None:
    response = client.get(companies_url)
    assert response.status_code == 200
    assert json.loads(response.content) == []


def test_one_company_exists_should_succedd(client) -> None:
    test_company = Company.objects.create(name="amazon")
    response = client.get(companies_url)
    response_content = json.loads(response.content)[0]
    assert response.status_code == 200
    assert response_content.get("name") == test_company.name
    assert response_content.get("status") == "Hiring"
    assert response_content.get("application_link") == ""
    assert response_content.get("notes") == ""

# ------------ Test Post Companies -----------------

def test_create_company_without_arguments_should_fail(client) -> None:
    response = client.post(path=companies_url)
    assert response.status_code == 400
    assert json.loads(response.content) == {"name": ["This field is required."]}


def test_create_existing_company_should_fail(client) -> None:
    Company.objects.create(name="Google")
    response = client.post(path=companies_url, data={"name":"Google"})
    assert response.status_code == 400
    assert json.loads(response.content) == {"name": ["company with this name already exists."]}


def test_create_company_with_only_name_all_fields_should_be_default(client) -> None:
    response = client.post(path=companies_url, data={"name": "teste name"})
    assert response.status_code == 201
    response_content = json.loads(response.content)
    assert response_content.get("name") == "teste name"
    assert response_content.get("status") == "Hiring"
    assert response_content.get("application_link") == ""
    assert response_content.get("notes") == ""

def test_create_company_with_layoffs_status_should_succeed(client) -> None:

    response = client.post(path=companies_url, data={"name": "teste name", "status":"layoffs"})
    assert response.status_code == 201
    response_content = json.loads(response.content)
    assert response_content.get("name")== "teste name"
    assert response_content.get("status")== "layoffs"
    assert response_content.get("application_link")== ""
    assert response_content.get("notes")== ""

@pytest.mark.xfail
def test_create_company_with_wrong_status_should_fail(client) -> None:
    response = client.post(path=companies_url, data={"name": "teste name", "status":"Wrong"})
    assert response.status_code == 400
    assert "Wrong" == str(response.content)
    assert "is not a valid choice" == str(response.content)

@pytest.mark.xfail
def test_should_be_ok_if_fails(self) -> None:
    self.assertEqual(1,2)


def raise_covid19_exception() -> None:
    raise ValueError("CoronaVirus Exception")

def test_raise_covid19_exception() -> None:
    with pytest.raises(ValueError) as e:
        raise_covid19_exception()
    assert "CoronaVirus Exception" == str(e.value)




import logging
logger = logging.getLogger("Corona_LOGS")

def funciton_that_logs_something() -> None:
    try:
        raise ValueError("CoronaVirus Exception")
    except ValueError as e:
        logger.warning(f"I am logging {str(e)}")

def test_logged_warning_level(caplog) -> None:
    funciton_that_logs_something()
    assert "I am logging CoronaVirus Exception" in caplog.text

def test_logged_info_level(caplog) -> None:
    with caplog.at_level(logging.INFO):
        logger.info("I am logging info level")
        assert "I am logging info level" in caplog.text