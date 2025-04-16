# frontend/Dockerfile

FROM node:22-alpine

WORKDIR /app

# Copia los archivos de dependencias primero (para usar la cache)
COPY package*.json ./

# Instala dependencias
RUN npm install

# Copia el resto del código del proyecto
COPY . .

# Inicia el servidor de desarrollo (Vue CLI)
CMD ["npm", "run", "serve"]
