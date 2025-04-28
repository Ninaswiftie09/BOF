
# Proyecto BOF - Backend (Django + DRF) & Frontend (Vue)

Este proyecto es una aplicación web compuesta por un backend en Django con Django Rest Framework y un frontend hecho en Vue.js. Utiliza PostgreSQL como base de datos y está completamente dockerizado para facilitar su despliegue y ejecución.

## 🚀 Requisitos...

Antes de comenzar, asegúrate de tener instalado lo siguiente:

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

## ⚙️ Estructura del proyecto

```
backup(miproyecto)/
├── backend/
│   ├── api/
│   └── proyecto_django/
├── frontend/
│   └── src/
├── docker-compose.yml
```

## 🐳 Cómo levantar el proyecto

1. Clona este repositorio:
```bash
git clone https://github.com/Ninaswiftie09/BOF.git
cd BOF
```

2. Lanza todos los servicios:
```bash
docker compose up --build
```

Esto levantará los siguientes contenedores:
- `django_backend`: Servidor Django en http://localhost:8000
- `vue_frontend`: Aplicación Vue.js en http://localhost:5173
- `postgres_db`: Base de datos PostgreSQL
- `pgadmin`: Interfaz gráfica para PostgreSQL en http://localhost:5050

## 🧪 Probar la API

Puedes probar si el backend está funcionando accediendo a:

```
http://localhost:8000/api/ping/
```

Y deberías recibir una respuesta como:
```json
{"message": "pong"}
```

## 🔧 Acceso a pgAdmin

- URL: http://localhost:5050
- Usuario: `admin@admin.com`
- Contraseña: `admin`

Recuerda agregar un servidor nuevo y usar estos datos para conectarte a PostgreSQL:

- Host: `db`
- Usuario: `user`
- Contraseña: `pass`
- Nombre de la base de datos: `proyecto`

Hecho por el equipo de BOF 💻..
