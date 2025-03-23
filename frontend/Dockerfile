# Use Node.js official image
FROM node:18

# Set working directory inside the container
WORKDIR /app

# Copy package.json and package-lock.json separately to optimize caching
COPY package.json package-lock.json ./

# Install dependencies inside the container
RUN npm install

# Copy the entire frontend source code AFTER installing dependencies
COPY . .

# Ensure vite is installed globally (optional but can help)
RUN npm install -g vite

# Expose the correct port for Vite
EXPOSE 5173

# Start Vite development server with proper host binding
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "5173"]
