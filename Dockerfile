# ------------------------------------------------
# Stage 1: Build the React frontend
# ------------------------------------------------
FROM node:20-alpine AS build-frontend
WORKDIR /usr/src/app

# Copy only the package.json and lock first for caching
COPY frontend/package*.json ./
RUN npm install

# Now copy the rest of the frontend
COPY frontend/ ./
RUN npm run build

# ------------------------------------------------
# Stage 2: Build the Python backend
# ------------------------------------------------
FROM python:3.12-slim
WORKDIR /app

# Copy requirements and install
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ /app

# Copy the built React files from Stage 1
# --> this is where your final index.html and static assets come from
COPY --from=build-frontend /usr/src/app/build/ /app/static/

# Expose the Flask port
EXPOSE 5000

CMD ["python", "run.py"]
    