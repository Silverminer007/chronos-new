# --- Build Stage ---
FROM node:20-alpine AS builder

# Set working directory
WORKDIR /app

# Install dependencies
COPY package.json package-lock.json* ./
RUN npm install

# Copy source files
COPY . .

# Build Nuxt 3 app
RUN npm run build

# --- Production Stage ---
FROM node:20-alpine

# Set working directory
WORKDIR /app

# Copy only necessary files from builder
COPY --from=builder /app/.output ./.output
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./

# Expose Nuxt port (default: 3000)
EXPOSE 3000

# Start Nuxt 3 server (SSR)
CMD ["node", ".output/server/index.mjs"]
