import pytest
from django.core.management import call_command
from django.core.management.base import CommandError

from products.models import Product

pytestmark = pytest.mark.django_db


def test_seed_creates_products():
    call_command("seed_products", force=True)
    assert Product.objects.count() > 0


def test_seed_is_idempotent():
    call_command("seed_products", force=True)
    first_count = Product.objects.count()

    call_command("seed_products", force=True)
    assert Product.objects.count() == first_count


def test_seed_reset_removes_existing_products():
    Product.objects.create(name="Temporary", price="1.00")

    call_command("seed_products", reset=True, force=True)

    assert not Product.objects.filter(name="Temporary").exists()


def test_seed_refused_when_debug_is_off(settings):
    settings.DEBUG = False
    with pytest.raises(CommandError):
        call_command("seed_products")