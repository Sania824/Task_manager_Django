from http.client import responses

from django.test import TestCase
import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Task

# Create your tests here.
def test_register_and_login(client):
    """Register the user"""
    register_response = client.post.reverse('register'),{
        'username': 'sania',
        'password1': 'StrongPassword123!',
        'password2': 'StrongPassword123!',
        'email': 'sania@gmail.com'
    }

    """Check if the user was created"""
    assert register_response.status_code == 302
    assert User.objects.filter(username='sania').exists()

    """Trying to login with the same credentials"""
    login_response = client.post.reverse('login'),{
        'username':'sania',
        'password':'StrongPassword123!'
    }
    assert login_response.status_code == 302

def test_create_task(client):
    create_response = client.post(reverse('task-create'),{
        'title':'Wash Dishes',
        'description':'Do dishes as soon as you get home',
        'complete':'False',
    }
    )
    assert create_response.status_code == 200
    assert User.objects.filter(title='Wash Dishes').exists()

def test_update_task(client):
    """First creating a user"""
    user = User.objects.create_user(username='testuser', password='testpass')
    client.login(username='testuser', password='testpass') # Logging the user in

    """Creating a task once the user is logged in so that the task is of that specific user"""
    task = Task.objects.create(user=user, title='Old Title', description='Old Desc', complete=False)

    update_data = {
        'title': 'New Title',
        'description': 'New Desc',
        'complete': True,
    }

    url = reverse('task-update', kwargs={'pk': task.id})
    response = client.post(url, update_data)

    task.refresh_from_db()

    assert response.status_code == 302  # Should redirect
    assert task.title == 'New Title'
    assert task.description == 'New Desc'
    assert task.complete is True

@pytest.mark.django.db
def test_unauthenticated_update_user(client):
    user = User.objects.create_user(username='testuser', password='testpass')
    task = Task.objects.create(user=user, title='Sample', description='Sample', complete=False)

    update_data = {
        'title': 'New Title',
        'description': 'New Desc',
        'complete': True,
    }

    url = reverse('task-update', kwargs={'pk':task.id})
    response = client.post(url, update_data)

    assert response.status_code == 302
    assert 'login/' in response.url

@pytest.mark.django_db
def test_task_delete(client):
    user = User.objects.create_user(username='sania', password='pwd12345')
    client.login(username='sania', password='pwd12345')

    task = Task.objects.create(user=user, title='buy groceries', description='none', complete=False)

    response = client.get(reverse('task-delete', kwargs={'pk': task.id}))
    assert response.url == reverse('tasks')
    with pytest.raises(Task.DoesNotExist):
        Task.objects.get(id=task.id)