"""
Backend de autenticación que NO duplica datos
Permite que fintech.User se autentique sin crear auth.User duplicado
"""

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from .models import User as FintechUser
import logging

logger = logging.getLogger(__name__)


class FintechAuthenticationBackend(ModelBackend):
    """
    Backend que permite autenticación de fintech.User sin duplicar datos
    Retorna fintech.User como si fuera auth.User
    """
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Autentica usuarios de fintech.User sin crear duplicados
        """
        if username is None or password is None:
            return None
        
        # 1. Intentar autenticar administradores (auth.User) - comportamiento normal
        try:
            auth_user = get_user_model().objects.get(username=username)
            if auth_user.check_password(password):
                logger.info(f"Administrador autenticado: {username}")
                return auth_user
        except get_user_model().DoesNotExist:
            pass
        
        # 2. Intentar autenticar clientes (fintech.User)
        try:
            fintech_user = FintechUser.objects.get(username=username)
            
            # Verificar contraseña del fintech.User
            if hasattr(fintech_user, 'password') and fintech_user.check_password(password):
                # Retornar fintech_user como si fuera auth.User
                logger.info(f"Cliente autenticado: {username}")
                return self._create_user_wrapper(fintech_user)
                
        except FintechUser.DoesNotExist:
            pass
        
        logger.warning(f"Intento de autenticación fallido para: {username}")
        return None
    
    def _create_user_wrapper(self, fintech_user):
        """
        Crea un wrapper que hace que fintech.User funcione como auth.User
        SIN duplicar datos
        """
        class UserWrapper:
            def __init__(self, fintech_user):
                self._fintech_user = fintech_user
                
                # Copiar atributos necesarios para Django
                self.id = fintech_user.id
                self.username = fintech_user.username
                self.email = getattr(fintech_user, 'email', '')
                self.first_name = getattr(fintech_user, 'first_name', '')
                self.last_name = getattr(fintech_user, 'last_name', '')
                self.is_active = getattr(fintech_user, 'is_active', True)
                self.is_staff = False  # Clientes no son staff
                self.is_superuser = False  # Clientes no son superusuarios
                self.date_joined = getattr(fintech_user, 'date_joined', None)
                
                # Guardar referencia al usuario original
                self._original_user = fintech_user
                self._is_fintech_user = True
            
            def check_password(self, password):
                """Verificar contraseña usando el fintech_user original"""
                return self._fintech_user.check_password(password)
            
            def get_user_permissions(self):
                """Permisos del usuario (clientes no tienen permisos especiales)"""
                return set()
            
            def get_group_permissions(self):
                """Permisos de grupo (clientes no tienen grupos)"""
                return set()
            
            def has_perm(self, perm):
                """Verificar permisos (clientes no tienen permisos especiales)"""
                return False
            
            def has_module_perms(self, app_label):
                """Verificar permisos de módulo (clientes no tienen permisos)"""
                return False
            
            def get_fintech_user(self):
                """Método para acceder al fintech_user original"""
                return self._fintech_user
            
            def __str__(self):
                return f"FintechUser({self.username})"
            
            def __repr__(self):
                return f"<UserWrapper: {self.username}>"
        
        return UserWrapper(fintech_user)
    
    def get_user(self, user_id):
        """
        Obtiene un usuario por ID
        """
        try:
            # Buscar en auth.User primero
            return get_user_model().objects.get(pk=user_id)
        except get_user_model().DoesNotExist:
            # Buscar en fintech.User
            try:
                fintech_user = FintechUser.objects.get(pk=user_id)
                return self._create_user_wrapper(fintech_user)
            except FintechUser.DoesNotExist:
                return None


class ClientAuthenticationBackend(ModelBackend):
    """
    Backend específico para clientes que busca por email o teléfono
    """
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Autentica clientes buscando por username, email o teléfono
        """
        if username is None or password is None:
            return None
        
        # Buscar cliente por username, email o teléfono
        try:
            from django.db import models
            client_user = FintechUser.objects.get(
                models.Q(username=username) |
                models.Q(email=username) |
                models.Q(phone_1__phone_number=username)
            )
            
            # Verificar contraseña
            if hasattr(client_user, 'password') and client_user.check_password(password):
                # Usar el mismo wrapper que el backend principal
                backend = FintechAuthenticationBackend()
                return backend._create_user_wrapper(client_user)
                
        except FintechUser.DoesNotExist:
            pass
        
        return None