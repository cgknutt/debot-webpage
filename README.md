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

- `lando yarn <command>` - Run yarn commands in the frontend service
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

### Accessing MongoDB

For local development, you can connect to MongoDB in several ways:

1. Using the MongoDB CLI through Lando:
   ```
   lando mongo
   ```

2. Using the MongoDB CLI directly through Docker:
   ```
   docker exec -it debot_database_1 mongosh
   ```

3. Using an external MongoDB client (like MongoDB Compass, Studio 3T, etc):
   - Host: localhost
   - Port: Run `lando info` and look for the database service port mapping
   - Database: debot
   - No authentication required for local development

You can run the `./health-check.sh` script to see the current MongoDB connection information.

## Accessing the Application Services

### Method 1: Direct Local URLs (Recommended)

The application can be accessed using direct local URLs with the port numbers assigned by Lando:

- Frontend: `http://localhost:<frontend-port>` (e.g., http://localhost:50871)
- Backend API: `http://localhost:<backend-port>` (e.g., http://localhost:50870)

These ports may change when containers are restarted. You can find the current ports with the command:

```bash
lando info
```

### Method 2: Lando Domain URLs

Alternatively, you can access the services via Lando domain URLs:

- Frontend: https://debot.lndo.site/
- Backend API: https://api.debot.lndo.site/

**Note:** The Lando domain URLs may experience issues due to proxy configuration. If you encounter problems, use the direct local URLs.

## Recent Updates: Improved Port Handling

To improve stability and minimize issues with changing ports, the following changes have been implemented:

1. **Relative API URLs**: The frontend now uses relative URLs for API requests, eliminating the need to hardcode backend ports in the configuration.

2. **Portforward Configuration**: Services are configured with `portforward: true` in the Lando configuration, ensuring more reliable access to services from the host.

3. **Frontend Configuration**: The frontend's Vite configuration uses internal Docker networking to reliably connect to the backend, with fallback options for direct access.

These changes mean:
- No more manual updates to configuration files when ports change
- More reliable communication between services
- Better developer experience with fewer connection issues

### Using the MongoDB Admin UI

For local development, you can access MongoDB through the MongoDB Admin UI:

- URL: http://mongo.debot.lndo.site
- No authentication required for local development

To connect to the database, use the following details:
- Connection Name: debot-local
- Host: database
- Port: 27017

If the MongoDB Admin UI is not working, you can still access MongoDB using the CLI or an external client as described above.
