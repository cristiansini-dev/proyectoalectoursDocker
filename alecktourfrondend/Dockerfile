# Imagen base
FROM node:22-alpine

# Carpeta de trabajo
WORKDIR /app

# Copiar package.json
COPY package*.json ./

# Instalar dependencias
RUN npm install

# Copiar proyecto
COPY . .

# Exponer puerto
EXPOSE 5173

# Ejecutar vite
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]