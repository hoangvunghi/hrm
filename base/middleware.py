from django.shortcuts import redirect
from django.urls import reverse
import logging

logger = logging.getLogger(__name__)

class CustomAdminMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_superuser:
            return self.get_response(request)

        if request.user.is_staff and request.path.startswith(reverse('admin:index')):
            return redirect('hr_admin:index')

        return self.get_response(request)
