# Debot Website

A simple text input application built with Vue 3 + FastAPI + MongoDB.

## Development with Lando

This project uses [Lando](https://lando.dev/) for local development. Lando is a free, open-source, cross-platform, local development environment tool built on Docker.

### Prerequisites

- [Lando](https://docs.lando.dev/getting-started/installation.html)
- [Docker](https://www.docker.com/products/docker-desktop/)

### Getting Started

1. Clone this repository:
   ```
   git clone <repository-url>
   cd debot-website
   ```

2. Start Lando:
   ```
   lando start
   ```
   This will start all services (frontend, backend, and MongoDB) in containers.

3. Access the application:
   - Frontend: https://debot.lndo.site:3000
   - Backend API: https://api.debot.lndo.site:8000
   - API Documentation: https://api.debot.lndo.site:8000/docs

### Useful Commands

- `lando npm <command>` - Run npm commands in the frontend service
- `lando python <command>` - Run Python commands in the backend service
- `lando pip <command>` - Run pip commands in the backend service
- `lando mongo` - Access the MongoDB shell

### Project Structure

- `/frontend` - Vue 3 frontend application
  - Uses Composition API with script setup
  - Pinia for state management
  - Axios for API requests
  
- `/backend` - FastAPI backend application
  - RESTful API endpoints
  - PyMongo for MongoDB connection
  - Pydantic models for data validation

### Application Flow

1. Enter text in the input field on the frontend
2. Click the submit button
3. The text is sent to the API and stored in MongoDB
4. The list below automatically updates with the new item
5. Items are displayed in reverse chronological order (newest first)
