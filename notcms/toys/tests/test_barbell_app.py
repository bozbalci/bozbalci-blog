from http import HTTPStatus

import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_barbell_app(client):
    url = reverse("toys:barbell-app")
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK
