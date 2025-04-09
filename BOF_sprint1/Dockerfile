FROM python:3.11-slim

# Establecer directorio de trabajo
FROM python:3.11-slim

# Establecer directorio de trabajo
WORKDIR /app

# Evitar que Python genere archivos .pyc
ENV PYTHONDONTWRITEBYTECODE=1
# Evitar que Python almacene en búfer la salida stdout y stderr
ENV PYTHONUNBUFFERED=1

# Instalar Django directamente (con comillas para evitar problemas con los símbolos)
RUN pip install --no-cache-dir "Django>=5.2,<5.3"

# Copiar el proyecto
COPY . .

# Exponer el puerto
EXPOSE 8000

# Comando para ejecutar el servidor
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]