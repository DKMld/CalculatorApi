import os
import pytest
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'calcApi.settings')
django.setup()

from django.contrib.auth.models import User
from django.urls import reverse
from calcApi.common.models import ApiRequest, ApiResponse


@pytest.mark.django_db
def test_admin_page_view(client):
    test_user = User.objects.create_user(username='testuser', password='testpass')

    client.login(username='testuser', password='testpass')

    api_request = ApiRequest.objects.create(user=test_user, request='test_request', file='test_file.csv')
    ApiResponse.objects.create(request=api_request, response='test_response')

    url = reverse('admin panel')
    response = client.get(url)

    assert response.status_code == 200

    assert 'user_requests' in response.context
    assert 'user_name' in response.context
    assert response.context['user_name'] == 'testuser'

    user_requests = response.context['user_requests']
    assert len(user_requests) == 1
    assert user_requests[0].request == 'test_request'
    assert user_requests[0].responses.first().response == 'test_response'