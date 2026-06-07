# Imagen base
FROM node:22-alpine

# Carpeta de trabajo
WORKDIR /app

# Copiar package.json y package-lock.json primero
COPY package*.json ./

# Instalar dependencias
RUN npm install

# Copiar el resto del proyecto
COPY . .

# Exponer puerto de Vite
EXPOSE 5173

# Ejecutar aplicación
CMD ["npm", "run", "dev", "--host"]