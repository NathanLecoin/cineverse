# Build stage
FROM node:18-alpine AS build

WORKDIR /app

# Copier package.json et package-lock.json
COPY package*.json ./

# Installer les dépendances
RUN npm install

# Copier le reste du code
COPY . .

# Build de production
RUN npm run build

# Production stage avec Nginx
FROM nginx:alpine

# Copier le build dans Nginx
COPY --from=build /app/dist /usr/share/nginx/html

# Copier la config Nginx personnalisée
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
