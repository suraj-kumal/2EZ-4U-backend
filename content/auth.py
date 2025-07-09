# myapp/authentication.py
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import AnonymousUser

class HardcodedTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.headers.get('Authorization')
        print(f"Received token: {token}")  # Debugging statement
        if not token:
            print("No token found in headers")
            return None

        expected_token = 'd86a715f865f41d622295540d4944c12'
        if token != expected_token:
            print("Invalid token")
            raise AuthenticationFailed('Invalid token')

        print("Token is valid")
        return (AnonymousUser(), token)  # Return an anonymous user or a custom user object

