# Use a lightweight Nginx image
FROM nginx:alpine

# Copy all project files to Nginx’s default web directory
COPY . /usr/share/nginx/html

# Expose port 80 to access the app
EXPOSE 80

# Run Nginx in the foreground
CMD ["nginx", "-g", "daemon off;"]
