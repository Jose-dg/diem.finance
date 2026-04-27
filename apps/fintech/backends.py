from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q


class ClientAuthenticationBackend(ModelBackend):
    """
    Permite autenticación por username, email o teléfono.
    Funciona directamente con fintech.User como AUTH_USER_MODEL.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None or password is None:
            return None

        User = get_user_model()
        try:
            user = User.objects.get(
                Q(username=username) |
                Q(email=username) |
                Q(phone_1__phone_number=username)
            )
        except User.DoesNotExist:
            return None
        except User.MultipleObjectsReturned:
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
