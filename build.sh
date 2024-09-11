#!/bin/sh

# Actualiza pip
python -m pip install --upgrade pip

# Instala las dependencias
pip install -r requirements.txt

# Ejecuta migraciones
python manage.py migrate

# Asegúrate de que la carpeta 'static' existe
mkdir -p static

# Recolecta archivos estáticos
python manage.py collectstatic --no-input

# Crea el superusuario si no existe
echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'password') if not User.objects.filter(username='admin').exists() else print('Superuser already exists')" | python manage.py shell
