import django
from django.conf import settings


def pytest_configure() -> None:
    settings.configure(
        INSTALLED_APPS=('tests',),
    )
    django.setup()
