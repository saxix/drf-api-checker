from django.urls import reverse

from drf_api_checker.pytest import contract


@contract()
def test_url(frozen_detail):
    url = reverse("master-list")
    return url
