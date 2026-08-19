# Usamos o Nginx, um servidor web super leve
FROM nginx:alpine

# Copiamos todos os nossos arquivos (HTML, CSS e JS) para a pasta pública do servidor
COPY . /usr/share/nginx/html/

# Expomos a porta padrão de sites
EXPOSE 80