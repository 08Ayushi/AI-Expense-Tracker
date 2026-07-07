"""Session auth without CSRF enforcement (SPA + React, same as Flask sessions)."""
from rest_framework.authentication import SessionAuthentication


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return
