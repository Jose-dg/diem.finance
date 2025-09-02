# 🔧 Pseudocódigo Detallado - Cambios a Implementar

## 🎯 **Resumen de Cambios**

Este documento detalla en pseudocódigo exactamente todos los cambios que vamos a implementar en el proyecto Django Fintech. Los cambios son **simples, seguros y mejorarán significativamente** la calidad del código.

---

## 📋 **CAMBIOS CRÍTICOS DE SEGURIDAD**

### **1. Configuración de Variables de Entorno**

#### **PSEUDOCÓDIGO: Crear archivo .env**
```bash
# PASO 1: Crear archivo .env en la raíz del proyecto
CREAR_ARCHIVO(".env") {
    ESCRIBIR_LÍNEA("SECRET_KEY=tu-secret-key-segura-aqui")
    ESCRIBIR_LÍNEA("DEBUG=False")
    ESCRIBIR_LÍNEA("CORS_ALLOW_ALL_ORIGINS=False")
    ESCRIBIR_LÍNEA("CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000")
    ESCRIBIR_LÍNEA("DATABASE_URL=postgresql://usuario:password@localhost:5432/fintech")
    ESCRIBIR_LÍNEA("REDIS_URL=redis://localhost:6379/0")
}
```

#### **PSEUDOCÓDIGO: Modificar core/settings.py**
```python
# PASO 2: Cambiar configuración de seguridad
ARCHIVO("core/settings.py") {
    
    # LÍNEA 19: Cambiar SECRET_KEY hardcodeada
    ANTES: SECRET_KEY = 'django-insecure-s%=f4!f-89o#gm3e%t2ss4$81xyk*e*%a#*)6#xi)o%_^rxo)x'
    DESPUÉS: SECRET_KEY = env('SECRET_KEY', default='django-insecure-change-me-in-production')
    
    # LÍNEA 22: Cambiar DEBUG
    ANTES: DEBUG = True
    DESPUÉS: DEBUG = env.bool('DEBUG', default=False)
    
    # LÍNEA 133: Cambiar CORS
    ANTES: CORS_ALLOW_ALL_ORIGINS = True
    DESPUÉS: CORS_ALLOW_ALL_ORIGINS = env.bool('CORS_ALLOW_ALL_ORIGINS', default=False)
    AGREGAR: CORS_ALLOWED_ORIGINS = env.list('CORS_ALLOWED_ORIGINS', default=[])
    
    # AGREGAR: Configuración AUTH_USER_MODEL
    AGREGAR_LÍNEA: AUTH_USER_MODEL = 'fintech.User'
}
```

---

## 🏗️ **CAMBIOS DE ARQUITECTURA DJANGO**

### **2. Corregir Uso de `get_user_model()`**

#### **PSEUDOCÓDIGO: Modificar apps/fintech/models.py**
```python
# PASO 3: Cambiar imports y referencias
ARCHIVO("apps/fintech/models.py") {
    
    # LÍNEAS 1-8: Limpiar imports
    ANTES: {
        from django.contrib.auth.models import AbstractUser, Group, Permission
        from django.db import models
        from django.contrib.auth import get_user_model  
        from django.db import transaction as db_transaction
        from django.db import models, transaction as db_transaction  # DUPLICADO
    }
    
    DESPUÉS: {
        from django.contrib.auth.models import AbstractUser, Group, Permission
        from django.db import models, transaction as db_transaction
        from django.utils import timezone
        from decimal import ROUND_HALF_UP, Decimal
        from django.conf import settings
        import uuid
        import math
        from datetime import timedelta
        from apps.fintech.managers import CreditManager, UserProfileManager, TransactionManager, InstallmentManager
    }
    
    # LÍNEA 73: Cambiar Address model
    ANTES: user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='addresses')
    DESPUÉS: user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='addresses')
    
    # LÍNEA 167: Cambiar Seller model
    ANTES: user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='seller_profile')
    DESPUÉS: user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='seller_profile')
    
    # LÍNEA 224: Cambiar Credit model - registered_by
    ANTES: registered_by = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, related_name='credits_registered')
    DESPUÉS: registered_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='credits_registered')
    
    # LÍNEA 539: Cambiar Expense model - registered_by
    ANTES: registered_by = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, related_name='expenses')
    DESPUÉS: registered_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='expenses')
    
    # LÍNEA 540: Cambiar Expense model - user
    ANTES: user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='expense_made_by')
    DESPUÉS: user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='expense_made_by')
}
```

### **3. Reorganizar INSTALLED_APPS**

#### **PSEUDOCÓDIGO: Modificar core/settings.py**
```python
# PASO 4: Reorganizar configuración de aplicaciones
ARCHIVO("core/settings.py") {
    
    # LÍNEAS 30-50: Reorganizar INSTALLED_APPS
    ANTES: {
        DJANGO_APPS = [
            'django.contrib.admin',
            'django.contrib.auth',
            # ...
        ]
        
        PROJECT_APPS = [
            'apps.fintech',
            'apps.dashboard'
        ]
        
        INSTALLED_APPS = [
            'django.contrib.admin',  # DUPLICADO
            'django.contrib.auth',   # DUPLICADO
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.messages',
            'django.contrib.staticfiles',
            'rest_framework',
            'corsheaders',
            'apps.fintech',          # DUPLICADO
            'apps.dashboard',        # DUPLICADO
            'apps.revenue',
            'apps.forecasting',
            'apps.insights',
        ]
    }
    
    DESPUÉS: {
        DJANGO_APPS = [
            'django.contrib.admin',
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.messages',
            'django.contrib.staticfiles',
        ]
        
        THIRD_PARTY_APPS = [
            'corsheaders',
            'rest_framework',
            'rest_framework.authtoken',
            'rest_framework_simplejwt',
            'rest_framework_simplejwt.token_blacklist',
            'django_filters',
        ]
        
        PROJECT_APPS = [
            'apps.fintech',
            'apps.dashboard',
            'apps.revenue',
            'apps.forecasting',
            'apps.insights',
        ]
        
        INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + PROJECT_APPS
    }
}
```

---

## 🗄️ **CAMBIOS DE MODELOS**

### **4. Implementar Properties para Campos Calculables**

#### **PSEUDOCÓDIGO: Modificar Credit Model**
```python
# PASO 5: Convertir campos calculables a properties
ARCHIVO("apps/fintech/models.py") {
    
    CLASE("Credit") {
        
        # LÍNEAS 235-236: Eliminar campos calculables
        ANTES: {
            total_abonos = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
            pending_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
        }
        
        DESPUÉS: {
            # Eliminar estos campos del modelo
            # Se calcularán como properties
        }
        
        # AGREGAR: Properties para cálculos
        AGREGAR_PROPERTY("total_abonos") {
            """
            Calcula el total de abonos realizados
            """
            RETORNAR self.payments.aggregate(
                total=Sum('amount_paid')
            )['total'] or Decimal('0.00')
        }
        
        AGREGAR_PROPERTY("pending_amount") {
            """
            Calcula el monto pendiente
            """
            RETORNAR self.price - self.total_abonos
        }
        
        AGREGAR_PROPERTY("percentage_paid") {
            """
            Calcula el porcentaje pagado del crédito
            """
            SI self.price Y self.price > 0:
                RETORNAR (self.total_abonos / self.price) * 100
            SINO:
                RETORNAR 0
        }
    }
}
```

### **5. Simplificar Método Save del Credit Model**

#### **PSEUDOCÓDIGO: Refactorizar método save**
```python
# PASO 6: Simplificar lógica de negocio en modelos
ARCHIVO("apps/fintech/models.py") {
    
    CLASE("Credit") {
        
        # LÍNEAS 400-500: Simplificar método save
        ANTES: {
            def save(self, *args, **kwargs):
                # Protección contra recursión infinita
                if hasattr(self, '_saving') and self._saving:
                    return super(Credit, self).save(*args, **kwargs)
                
                self._saving = True
                
                try:
                    with db_transaction.atomic():
                        # ... lógica compleja de cálculo
                        pass
                finally:
                    self._saving = False
        }
        
        DESPUÉS: {
            def save(self, *args, **kwargs):
                # Lógica mínima en el modelo
                super().save(*args, **kwargs)
                # Delegar cálculos complejos al servicio
                CreditCalculationService.update_credit_totals(self)
        }
    }
}
```

---

## 🔧 **CAMBIOS DE CÓDIGO**

### **6. Crear Servicios para Lógica de Negocio**

#### **PSEUDOCÓDIGO: Crear CreditCalculationService**
```python
# PASO 7: Crear servicio para cálculos de crédito
CREAR_ARCHIVO("apps/fintech/services/credit/credit_calculation_service.py") {
    
    CLASE("CreditCalculationService") {
        
        MÉTODO_ESTÁTICO("calculate_credit_metrics", credit) {
            """
            Calcula métricas del crédito
            """
            installments = credit.installments.all()
            payments = AccountMethodAmount.objects.filter(credit=credit)
            
            total_paid = sum(p.amount_paid for p in payments)
            overdue_installments = installments.filter(status='overdue')
            
            RETORNAR {
                'total_amount': credit.price,
                'total_paid': total_paid,
                'remaining_amount': credit.pending_amount,
                'installment_count': installments.count(),
                'paid_installments': installments.filter(status='paid').count(),
                'overdue_installments': overdue_installments.count(),
                'total_overdue_days': sum(i.days_overdue for i in overdue_installments),
                'late_fees': CreditService.calculate_late_fees(credit),
                'morosidad_level': credit.morosidad_level,
                'is_in_default': credit.is_in_default
            }
        }
        
        MÉTODO_ESTÁTICO("update_credit_totals", credit) {
            """
            Actualiza totales del crédito
            """
            # Lógica de actualización aquí
            # Mover lógica compleja del modelo save() aquí
        }
    }
}
```

### **7. Actualizar Imports en Otros Archivos**

#### **PSEUDOCÓDIGO: Actualizar imports**
```python
# PASO 8: Actualizar imports en otros archivos
ARCHIVO("apps/fintech/views.py") {
    # LÍNEA 8: Cambiar import
    ANTES: from django.contrib.auth import get_user_model
    DESPUÉS: from django.conf import settings
}

ARCHIVO("apps/fintech/serializers.py") {
    # LÍNEA 1: Cambiar import
    ANTES: from django.contrib.auth import get_user_model
    DESPUÉS: from django.conf import settings
    
    # LÍNEA 9: Cambiar asignación
    ANTES: User = get_user_model()
    DESPUÉS: User = apps.get_model(settings.AUTH_USER_MODEL)
}
```

---

## 🧪 **CAMBIOS DE TESTING**

### **8. Actualizar Tests**

#### **PSEUDOCÓDIGO: Actualizar tests**
```python
# PASO 9: Actualizar tests para usar properties
ARCHIVO("apps/fintech/tests/test_credit_lifecycle.py") {
    
    CLASE("CreditLifecycleTestCase") {
        
        MÉTODO("test_credit_creation_calculations") {
            # Crear crédito
            credit = Credit.objects.create(**self.credit_data)
            
            # Verificar cálculos automáticos usando properties
            ASSERT_EQUAL(credit.pending_amount, credit.price)
            ASSERT_EQUAL(credit.earnings, credit.price - credit.cost)
            ASSERT_EQUAL(credit.installment_number, 3)
            ASSERT_NOT_NONE(credit.installment_value)
            
            # Verificar que se generaron las cuotas
            installments = credit.installments.all()
            ASSERT_EQUAL(installments.count(), 3)
        }
        
        MÉTODO("test_payment_flow_on_time") {
            credit = Credit.objects.create(**self.credit_data)
            installment = credit.installments.first()
            
            # Realizar pago puntual
            payment_amount = installment.amount
            
            # Crear transacción de pago
            transaction = Transaction.objects.create(
                transaction_type='income',
                user=self.user,
                category=self.subcategory,
                description='Pago puntual',
                date=timezone.now()
            )
            
            # Crear método de pago
            payment_method = AccountMethodAmount.objects.create(
                payment_method=self.payment_account,
                payment_code=f'PAY_{transaction.uid}',
                amount=payment_amount,
                amount_paid=payment_amount,
                credit=credit,
                transaction=transaction
            )
            
            # Verificar actualizaciones usando properties
            credit.refresh_from_db()
            installment.refresh_from_db()
            
            ASSERT_EQUAL(credit.total_abonos, payment_amount)
            ASSERT_EQUAL(credit.pending_amount, credit.price - payment_amount)
            ASSERT_TRUE(installment.paid)
            ASSERT_EQUAL(installment.status, 'paid')
        }
    }
}
```

---

## 📋 **CHECKLIST DE IMPLEMENTACIÓN**

### **PSEUDOCÓDIGO: Plan de Ejecución**
```bash
# PASO 1: Preparación
FUNCIÓN("preparación") {
    EJECUTAR("git status")  # Verificar estado del repositorio
    EJECUTAR("git checkout -b feature/refactor-user-model")  # Crear rama
    EJECUTAR("python3 manage.py check")  # Verificar estado actual
    EJECUTAR("python3 manage.py showmigrations")  # Verificar migraciones
}

# PASO 2: Cambios de Seguridad
FUNCIÓN("cambios_seguridad") {
    CREAR_ARCHIVO(".env")  # Crear archivo de variables de entorno
    MODIFICAR("core/settings.py") {
        CAMBIAR_SECRET_KEY()
        CAMBIAR_DEBUG()
        CAMBIAR_CORS()
        AGREGAR_AUTH_USER_MODEL()
    }
}

# PASO 3: Cambios de Arquitectura
FUNCIÓN("cambios_arquitectura") {
    MODIFICAR("apps/fintech/models.py") {
        LIMPIAR_IMPORTS()
        CAMBIAR_GET_USER_MODEL()
        REORGANIZAR_INSTALLED_APPS()
    }
}

# PASO 4: Cambios de Modelos
FUNCIÓN("cambios_modelos") {
    MODIFICAR("apps/fintech/models.py") {
        IMPLEMENTAR_PROPERTIES()
        SIMPLIFICAR_SAVE_METHOD()
    }
    CREAR_SERVICIOS()
}

# PASO 5: Validación
FUNCIÓN("validación") {
    EJECUTAR("python3 manage.py check")
    EJECUTAR("python3 manage.py makemigrations --dry-run")
    EJECUTAR("python3 manage.py test")
    EJECUTAR("python3 manage.py validate")
}

# PASO 6: Deploy
FUNCIÓN("deploy") {
    EJECUTAR("git add .")
    EJECUTAR("git commit -m 'Refactor: Mejorar arquitectura y seguridad'")
    EJECUTAR("git push origin feature/refactor-user-model")
    # Crear Pull Request
    # Revisar cambios
    # Merge a main
    # Deploy a producción
}
```

---

## ⏱️ **CRONOGRAMA DETALLADO**

### **PSEUDOCÓDIGO: Timeline de Implementación**
```bash
# DÍA 1: Seguridad (30 minutos)
TIEMPO("09:00 - 09:30") {
    CREAR_ARCHIVO(".env")
    MODIFICAR_SECURITY_SETTINGS()
    VALIDAR_CAMBIOS()
}

# DÍA 1: Arquitectura (1 hora)
TIEMPO("10:00 - 11:00") {
    CAMBIAR_GET_USER_MODEL()
    REORGANIZAR_INSTALLED_APPS()
    LIMPIAR_IMPORTS()
    VALIDAR_CAMBIOS()
}

# DÍA 2: Modelos (2 horas)
TIEMPO("09:00 - 11:00") {
    IMPLEMENTAR_PROPERTIES()
    SIMPLIFICAR_SAVE_METHOD()
    CREAR_SERVICIOS()
    VALIDAR_CAMBIOS()
}

# DÍA 2: Testing (1 hora)
TIEMPO("14:00 - 15:00") {
    ACTUALIZAR_TESTS()
    EJECUTAR_TESTS_COMPLETOS()
    VALIDAR_FUNCIONALIDAD()
}

# DÍA 3: Deploy (30 minutos)
TIEMPO("09:00 - 09:30") {
    DEPLOY_STAGING()
    VALIDAR_STAGING()
    DEPLOY_PRODUCCIÓN()
    VALIDAR_PRODUCCIÓN()
}
```

---

## 🎯 **RESULTADO ESPERADO**

### **PSEUDOCÓDIGO: Estado Final**
```python
# DESPUÉS DE LOS CAMBIOS:

# 1. Configuración Segura
ARCHIVO("core/settings.py") {
    SECRET_KEY = env('SECRET_KEY')  # ✅ Seguro
    DEBUG = env.bool('DEBUG', default=False)  # ✅ Seguro
    CORS_ALLOW_ALL_ORIGINS = env.bool('CORS_ALLOW_ALL_ORIGINS', default=False)  # ✅ Seguro
    AUTH_USER_MODEL = 'fintech.User'  # ✅ Configurado
}

# 2. Código Limpio
ARCHIVO("apps/fintech/models.py") {
    # Imports limpios
    from django.conf import settings  # ✅ Correcto
    
    # Referencias correctas
    user = models.ForeignKey(settings.AUTH_USER_MODEL, ...)  # ✅ Correcto
    
    # Properties para cálculos
    @property
    def total_abonos(self):  # ✅ Calculable
        return self.payments.aggregate(total=Sum('amount_paid'))['total'] or Decimal('0.00')
    
    @property
    def pending_amount(self):  # ✅ Calculable
        return self.price - self.total_abonos
}

# 3. Lógica de Negocio Separada
ARCHIVO("apps/fintech/services/credit/credit_calculation_service.py") {
    class CreditCalculationService:  # ✅ Servicio dedicado
        @staticmethod
        def update_credit_totals(credit):
            # Lógica compleja aquí
            pass
}

# 4. Tests Actualizados
ARCHIVO("apps/fintech/tests/test_credit_lifecycle.py") {
    # Tests que usan properties
    self.assertEqual(credit.total_abonos, expected_amount)  # ✅ Usa property
    self.assertEqual(credit.pending_amount, expected_pending)  # ✅ Usa property
}
```

---

## 💡 **BENEFICIOS INMEDIATOS**

### **PSEUDOCÓDIGO: Beneficios Esperados**
```python
BENEFICIOS = {
    "seguridad": {
        "SECRET_KEY": "Ya no está hardcodeada",
        "DEBUG": "Deshabilitado en producción",
        "CORS": "Configurado correctamente"
    },
    "código": {
        "get_user_model": "Eliminado del código",
        "imports": "Limpios y organizados",
        "consistencia": "Todos usan settings.AUTH_USER_MODEL"
    },
    "performance": {
        "cálculos": "Usan properties en lugar de campos",
        "consultas": "Más eficientes",
        "memoria": "Menos overhead"
    },
    "mantenibilidad": {
        "lógica_negocio": "Separada en servicios",
        "código": "Más limpio y legible",
        "tests": "Más robustos"
    }
}
```

---

## 🚀 **PRÓXIMOS PASOS**

### **PSEUDOCÓDIGO: Plan de Acción**
```bash
# INMEDIATO (Hoy)
EJECUTAR("preparación")
EJECUTAR("cambios_seguridad")
EJECUTAR("cambios_arquitectura")

# MAÑANA
EJECUTAR("cambios_modelos")
EJECUTAR("validación")

# PASADO MAÑANA
EJECUTAR("deploy")

# RESULTADO
PRINT("✅ Proyecto más seguro, limpio y mantenible")
PRINT("✅ Código que cumple con mejores prácticas Django")
PRINT("✅ Base de datos sin cambios (seguro para producción)")
```

**¿Estás listo para comenzar con la implementación paso a paso?**
