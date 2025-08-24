# FastApiReactAiGame - Dockerized Setup

This project contains a FastAPI backend, a React frontend, and can connect to an AI model service. The backend and frontend are orchestrated using Docker Compose. The AI model service can be provided remotely or run locally using Docker's model runner.

## Prerequisites
- [Docker](https://www.docker.com/products/docker-desktop) installed
- [Docker Compose](https://docs.docker.com/compose/) (if not included with Docker Desktop)

## Project Structure
- `backend/` - FastAPI backend
- `frontend/` - React frontend
- `docker-compose.yml` - Orchestrates backend and frontend services
- `Dockerfile.backend` - Backend Docker image
- `Dockerfile.frontend` - Frontend Docker image

## AI Model Service
- The backend requires access to an AI model service for story generation.
- You can use a remote AI model endpoint if available, or run a supported model locally using Docker's model runner.
- **To run a local model:**
  ```sh
  docker model run ai/qwen2.5:1.5B-F16
  ```
  (Replace with your required model and options.)
- Ensure your backend is configured to connect to the correct model endpoint (update environment variables as needed).
- If you have a remote AI service, set the backend's `OPENAI_CONNECTION_SERVICE_URL` to the remote endpoint.

## Setup Steps

1. **Clone the repository**

2. **Environment Variables**
    - Copy `backend/.env.example` to `backend/.env` and adjust as needed for your environment and model endpoint.

3. **Build and Start Backend and Frontend**
   ```sh
   docker-compose up --build
   ```
   This will start:
    - FastAPI backend (http://localhost:8000)
    - React frontend (http://localhost:5173)

4. **Access the Application**
    - Frontend: [http://localhost:5173](http://localhost:5173)
    - Backend API docs: [http://localhost:8000/docs](http://localhost:8000/docs)

5. **Stopping the Services**
   ```sh
   docker-compose down
   ```

## Notes
- If you use a local AI model, ensure it is running before starting the backend.
- Update the backend's environment variables to point to the correct AI model endpoint.

---

## Troubleshooting
- If you encounter port conflicts, change the ports in `docker-compose.yml`.
- For model connection issues, ensure the model service is running and accessible from the backend.

---
## Credits

This project idea is based on a tutorial from [YouTube](https://www.youtube.com/watch?v=_1P0Uqk50Ps&t=10468s).  
All rights to the original creator.
This modified and enhanced version to provide a fully Dockerized application setup, improved environment management, and streamlined development workflow.

---

## License
MIT License
