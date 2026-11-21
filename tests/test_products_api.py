import uuid

import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from products.models import Product

pytestmark = pytest.mark.django_db


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def product():
    return Product.objects.create(name="Keyboard", description="Mechanical", price="49.90", stock=10)


def test_list_empty(api_client):
    res = api_client.get(reverse("product-list"))
    assert res.status_code == 200
    assert res.json()["count"] == 0


def test_list_returns_products(api_client, product):
    res = api_client.get(reverse("product-list"))
    assert res.json()["count"] == 1
    assert res.json()["results"][0]["name"] == "Keyboard"


def test_create_product(api_client):
    payload = {"name": "Mouse", "description": "Wireless", "price": "19.99", "stock": 5}
    res = api_client.post(reverse("product-list"), payload, format="json")
    assert res.status_code == 201
    assert res.json()["price"] == "19.99"
    assert Product.objects.count() == 1


def test_create_rejects_negative_price(api_client):
    payload = {"name": "Mouse", "price": "-5", "stock": 5}
    res = api_client.post(reverse("product-list"), payload, format="json")
    assert res.status_code == 400
    body = res.json()["error"]
    assert body["code"] == "validation_error"
    assert "price" in body["details"]


def test_create_rejects_short_name(api_client):
    res = api_client.post(reverse("product-list"), {"name": "ab", "price": "1.00"}, format="json")
    assert res.status_code == 400
    assert "name" in res.json()["error"]["details"]


def test_retrieve_product(api_client, product):
    res = api_client.get(reverse("product-detail", args=[product.id]))
    assert res.status_code == 200
    assert res.json()["id"] == str(product.id)


def test_retrieve_not_found(api_client):
    res = api_client.get(reverse("product-detail", args=[uuid.uuid4()]))
    assert res.status_code == 404
    assert res.json()["error"]["code"] == "not_found"


def test_update_product(api_client, product):
    payload = {"name": "Keyboard Pro", "description": "RGB", "price": "79.90", "stock": 3}
    res = api_client.put(reverse("product-detail", args=[product.id]), payload, format="json")
    assert res.status_code == 200
    product.refresh_from_db()
    assert product.name == "Keyboard Pro"


def test_delete_product(api_client, product):
    res = api_client.delete(reverse("product-detail", args=[product.id]))
    assert res.status_code == 204
    assert not Product.objects.filter(id=product.id).exists()


def test_health_endpoints(api_client):
    assert api_client.get("/health/").status_code == 200
    assert api_client.get("/health/live/").status_code == 200
    assert api_client.get("/health/ready/").status_code == 200