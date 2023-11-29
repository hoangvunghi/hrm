from django.shortcuts import redirect
from django.urls import reverse
import logging

logger = logging.getLogger(__name__)

class CustomAdminMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith(reverse('hr_admin:index')) and request.user.is_superuser:
            return self.get_response(request)
        
        elif request.user.is_staff:
            hr_admin_group = request.user.groups.filter(name='HRAdminGroup').exists()

            if request.path.startswith(reverse('hr_admin:index')) and hr_admin_group:
                logger.info(f"User {request.user} is in HRAdminGroup")
                return self.get_response(request)
            else:
                return self.get_response(request)

        else:
            return self.get_response(request)
